import frappe
from frappe import _
from .exceptions import (
    OriginalInvoiceNotFoundError,
    InvalidInvoiceStateError,
    InvalidReturnQuantityError,
    ItemNotReturnableError
)

def validate_original_invoice(invoice_name, for_update=False):
    """
    Validates and fetches the original invoice.
    Uses for_update=True during final submission to prevent concurrent exchanges.
    """
    # for_update locks the row to prevent concurrent exchanges
    invoice = frappe.get_doc("POS Invoice", invoice_name, for_update=for_update)
    
    if not invoice:
        raise OriginalInvoiceNotFoundError(_("Original Invoice {0} not found").format(invoice_name))
        
    if invoice.docstatus != 1:
        raise InvalidInvoiceStateError(_("Original Invoice {0} must be submitted").format(invoice_name))
        
    if invoice.is_return:
        raise InvalidInvoiceStateError(_("Invoice {0} is already a return document").format(invoice_name))
        
    return invoice

def calculate_remaining_returnable_qty(original_invoice):
    """
    Calculates exactly how much of each item in the original invoice can still be returned.
    """
    # Find all submitted return invoices against this original invoice
    returned_items = frappe.get_all(
        "POS Invoice Item",
        filters={
            "parent": ["in", frappe.get_all("POS Invoice", filters={"return_against": original_invoice.name, "docstatus": 1}, pluck="name")]
        },
        fields=["item_code", "qty"]
    )
    
    already_returned = {}
    for item in returned_items:
        # returned qty is negative in POS Invoice Item, so we use abs()
        already_returned[item.item_code] = already_returned.get(item.item_code, 0) + abs(item.qty)
        
    remaining = {}
    for item in original_invoice.items:
        total_qty = item.qty
        returned = already_returned.get(item.item_code, 0)
        remaining[item.item_code] = remaining.get(item.item_code, 0) + (total_qty - returned)
        
    return remaining

def validate_return_request(original_invoice, return_items, remaining_qty_map):
    """
    Validates that the requested return items exist and do not exceed remaining qty.
    return_items should be a list of dicts: [{'item_code': 'X', 'qty': 1, 'serial_no': '...', 'batch_no': '...'}, ...]
    """
    for req_item in return_items:
        item_code = req_item.get("item_code")
        qty = float(req_item.get("qty", 0))
        
        if qty <= 0:
            raise InvalidReturnQuantityError(_("Return quantity must be greater than zero for item {0}").format(item_code))
            
        if item_code not in remaining_qty_map:
            raise ItemNotReturnableError(_("Item {0} was not in the original invoice").format(item_code))
            
        remaining = remaining_qty_map.get(item_code, 0)
        
        if qty > remaining:
            raise InvalidReturnQuantityError(
                _("Cannot return {0} of {1}. Only {2} remaining.").format(qty, item_code, remaining)
            )
            
        # Deduct from map to handle multiple rows of the same item
        remaining_qty_map[item_code] -= qty

def validate_new_items(new_items):
    """
    Basic validation for new items.
    """
    for item in new_items:
        if float(item.get("qty", 0)) <= 0:
            raise frappe.ValidationError(_("New sale quantity must be positive for item {0}").format(item.get("item_code")))

def validate_payments(payment_mode_amounts, difference):
    """
    Validates that the payment amounts sum up to the difference.
    difference > 0 means customer pays.
    difference < 0 means customer refund.
    difference == 0 means exact exchange.
    """
    total_payment = sum(float(p.get("amount", 0)) for p in payment_mode_amounts)
    
    if abs(total_payment - difference) > 0.01:
        from .exceptions import PaymentMismatchError
        raise PaymentMismatchError(
            _("Total payment amount ({0}) must equal the exchange difference ({1})").format(total_payment, difference)
        )
