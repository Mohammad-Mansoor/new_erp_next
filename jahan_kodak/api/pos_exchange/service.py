import frappe
from frappe import _
import json

from .idempotency import check_idempotency
from .validators import (
    validate_original_invoice,
    calculate_remaining_returnable_qty,
    validate_return_request,
    validate_new_items,
    validate_payments
)
from .return_handler import create_return_invoice
from .sales_handler import create_replacement_invoice
from .calculator import calculate_exchange_difference
from .payment_handler import apply_settlement

def _build_exchange_context(payload, for_update=False):
    """
    Shared calculation/building logic.
    Builds the in-memory documents and calculates differences.
    """
    if isinstance(payload, str):
        payload = json.loads(payload)
        
    original_invoice_name = payload.get("original_invoice")
    return_items = payload.get("return_items", [])
    new_items = payload.get("new_items", [])
    
    # 1. Validate original invoice
    original_invoice = validate_original_invoice(original_invoice_name, for_update=for_update)
    
    # 2. Concurrency protection: Recalculate remaining quantities
    remaining_qty_map = calculate_remaining_returnable_qty(original_invoice)
    
    # 3. Validate return request against actual remaining quantities
    validate_return_request(original_invoice, return_items, remaining_qty_map)
    
    # 4. Validate new items
    validate_new_items(new_items)
    
    # 5. Create Draft Invoices (in-memory)
    return_doc = None
    new_doc = None
    
    if return_items:
        return_doc = create_return_invoice(original_invoice, return_items)
        
    if new_items:
        new_doc = create_replacement_invoice(original_invoice, new_items)
        
    # 6. Calculate authoritative difference
    return_total, new_total, difference = calculate_exchange_difference(return_doc, new_doc)
    
    return {
        "original_invoice": original_invoice,
        "return_doc": return_doc,
        "new_doc": new_doc,
        "return_total": return_total,
        "new_total": new_total,
        "difference": difference,
        "return_items": return_items,
        "new_items": new_items,
        "payload": payload
    }

@frappe.whitelist()
def calculate_exchange(payload):
    """
    Preview-only endpoint for the frontend.
    Does not mutate the database.
    """
    if isinstance(payload, str):
        payload = json.loads(payload)
        
    context = _build_exchange_context(payload, for_update=False)
    
    difference = context["difference"]
    settlement_type = "exact"
    if difference > 0.001:
        settlement_type = "customer_pays"
    elif difference < -0.001:
        settlement_type = "customer_refund"
        
    payment_methods = []
    if settlement_type == "customer_pays":
        # Fetch payment methods for POS Profile
        pos_profile = context["original_invoice"].pos_profile
        profile_doc = frappe.get_doc("POS Profile", pos_profile)
        for pm in profile_doc.payments:
            payment_methods.append({
                "mode_of_payment": pm.mode_of_payment,
                "default": pm.default
            })
            
    # Also fetch the items' rates and amounts for the frontend
    replacement_items_preview = []
    if context["new_doc"]:
        for item in context["new_doc"].items:
            replacement_items_preview.append({
                "item_code": item.item_code,
                "qty": item.qty,
                "rate": item.rate,
                "amount": item.amount,
                "discount_amount": item.discount_amount
            })
            
    return {
        "return_total": context["return_total"],
        "replacement_total": context["new_total"],
        "difference": difference,
        "settlement_type": settlement_type,
        "currency": context["original_invoice"].currency,
        "payment_required": settlement_type != "exact",
        "payment_methods": payment_methods,
        "replacement_items_preview": replacement_items_preview
    }

@frappe.whitelist()
def process_exchange(payload):
    """
    The atomic entry point for the POS Exchange Workflow.
    """
    if isinstance(payload, str):
        payload = json.loads(payload)
        
    idempotency_key = payload.get("idempotency_key")
    customer_payments = payload.get("payments", [])
    
    # Check Idempotency before locking anything
    existing = check_idempotency(payload)
    if existing:
        return {"status": "success", "exchange_id": existing, "message": _("Exchange already completed.")}

    # All database operations must happen in a single transaction
    savepoint = "pos_exchange_start"
    frappe.db.savepoint(savepoint)
    
    try:
        context = _build_exchange_context(payload, for_update=True)
        
        return_doc = context["return_doc"]
        new_doc = context["new_doc"]
        difference = context["difference"]
        
        # 7. Validate frontend payment matches actual difference
        validate_payments(customer_payments, difference)
        
        # 8. Apply Settlement
        apply_settlement(return_doc, new_doc, difference, customer_payments)
        
        # 9. Insert and Submit documents
        return_invoice_name = None
        new_invoice_name = None
        
        if return_doc:
            return_doc.insert(ignore_permissions=True)
            return_doc.submit()
            return_invoice_name = return_doc.name
            
        if new_doc:
            new_doc.insert(ignore_permissions=True)
            new_doc.submit()
            new_invoice_name = new_doc.name
            
        # 10. Create the POS Exchange audit record
        from .idempotency import generate_payload_hash
        exchange_doc = frappe.new_doc("POS Exchange")
        exchange_doc.idempotency_key = idempotency_key
        exchange_doc.payload_hash = generate_payload_hash(payload)
        exchange_doc.original_invoice = context["original_invoice"].name
        exchange_doc.return_invoice = return_invoice_name
        exchange_doc.replacement_invoice = new_invoice_name
        exchange_doc.customer = context["original_invoice"].customer
        exchange_doc.company = context["original_invoice"].company
        exchange_doc.pos_profile = context["original_invoice"].pos_profile
        exchange_doc.status = "Completed"
        exchange_doc.return_total = context["return_total"]
        exchange_doc.replacement_total = context["new_total"]
        exchange_doc.difference = difference
        
        # Extract item details from the generated draft invoices
        return_items_details = {}
        if return_doc:
            for item in return_doc.items:
                return_items_details[item.item_code] = {
                    "item_name": item.item_name,
                    "rate": item.rate,
                    "amount": abs(item.amount)  # Return amount is negative in invoice
                }
                
        new_items_details = {}
        if new_doc:
            for item in new_doc.items:
                new_items_details[item.item_code] = {
                    "item_name": item.item_name,
                    "rate": item.rate,
                    "amount": item.amount
                }

        # Add Items to Exchange Record
        for r in context["return_items"]:
            details = return_items_details.get(r.get("item_code"), {})
            exchange_doc.append("items", {
                "type": "Return",
                "item_code": r.get("item_code"),
                "item_name": details.get("item_name"),
                "qty": r.get("qty"),
                "rate": details.get("rate", 0.0),
                "amount": details.get("amount", 0.0),
                "is_return": 1
            })
            
        for n in context["new_items"]:
            details = new_items_details.get(n.get("item_code"), {})
            exchange_doc.append("items", {
                "type": "New Sale",
                "item_code": n.get("item_code"),
                "item_name": details.get("item_name"),
                "qty": n.get("qty"),
                "rate": details.get("rate", 0.0),
                "amount": details.get("amount", 0.0),
                "is_return": 0
            })
            
        # Add Payments to Exchange Record
        for p in customer_payments:
            exchange_doc.append("payments", {
                "mode_of_payment": p.get("mode_of_payment"),
                "amount": p.get("amount")
            })
            
        # Insert will fail here if idempotency_key is duplicate due to MariaDB unique constraint
        exchange_doc.insert(ignore_permissions=True)
        exchange_doc.submit()
        
        return {
            "status": "success",
            "exchange_id": exchange_doc.name,
            "return_invoice": return_invoice_name,
            "new_invoice": new_invoice_name,
            "difference": difference,
            "original_invoice": context["original_invoice"].name,
            "settlement_type": "exact" if abs(difference) < 0.001 else ("customer_pays" if difference > 0.001 else "customer_refund")
        }
    except Exception as e:
        frappe.db.rollback(save_point=savepoint)
        raise e

@frappe.whitelist()
def get_remaining_returnable_qty(original_invoice_name):
    """
    Frontend endpoint to get remaining returnable quantities.
    """
    original_invoice = frappe.get_doc("POS Invoice", original_invoice_name)
    return calculate_remaining_returnable_qty(original_invoice)
