import frappe
from frappe import _
from frappe.utils import flt

def get_default_mop(pos_profile):
    """
    Retrieves the default Mode of Payment for the POS Profile.
    """
    if not pos_profile:
        return "Cash"
        
    mops = frappe.get_all(
        "POS Payment Method",
        filters={"parent": pos_profile},
        fields=["mode_of_payment", "default"],
        order_by="`default` desc"
    )
    
    if not mops:
        return "Cash"
        
    for mop in mops:
        if mop.default:
            return mop.mode_of_payment
            
    return mops[0].mode_of_payment

def get_pos_profile_mops(pos_profile):
    """
    Retrieves the list of valid Mode of Payment names configured for the POS Profile.
    """
    if not pos_profile:
        return []
    return frappe.get_all(
        "POS Payment Method",
        filters={"parent": pos_profile},
        pluck="mode_of_payment"
    )

def add_payment_to_doc(doc, mop, amt):
    """
    Helper to add payment amount to doc.payments, combining with existing row if same MOP.
    """
    amt = flt(amt)
    if not amt:
        return
    found = False
    for p in doc.payments:
        if p.mode_of_payment == mop:
            p.amount = flt(p.amount) + amt
            found = True
            break
    if not found:
        doc.append("payments", {"mode_of_payment": mop, "amount": amt})

def apply_settlement(return_doc, new_doc, difference, customer_payments):
    """
    Settles both invoices using standard ERPNext accounting.
    
    We use the POS Profile's default Mode of Payment for the 'internal' clearing of the exchange,
    and apply the actual customer payments (or refunds) to handle the difference.
    """
    pos_profile = return_doc.pos_profile if return_doc else (new_doc.pos_profile if new_doc else None)
    if not pos_profile:
        return
        
    default_mop = get_default_mop(pos_profile)
    valid_mops = get_pos_profile_mops(pos_profile)
    
    # 1. Clear out the original payments from return_doc and new_doc
    if return_doc:
        return_doc.set("payments", [])
        return_doc.paid_amount = 0
        
    if new_doc:
        new_doc.set("payments", [])
        new_doc.paid_amount = 0

    return_total = abs(return_doc.grand_total) if return_doc else 0.0
    new_total = new_doc.grand_total if new_doc else 0.0

    if difference == 0:
        # Exact exchange: settle both entirely with the default MOP (zero net effect on cash)
        if return_doc and return_total > 0:
            add_payment_to_doc(return_doc, default_mop, -return_total)
            return_doc.paid_amount = -return_total
        if new_doc and new_total > 0:
            add_payment_to_doc(new_doc, default_mop, new_total)
            new_doc.paid_amount = new_total
            
    elif difference > 0:
        # Customer pays:
        # Return invoice is settled entirely with default MOP
        if return_doc and return_total > 0:
            add_payment_to_doc(return_doc, default_mop, -return_total)
            return_doc.paid_amount = -return_total
            
        # New invoice is settled with default MOP up to the return_total, plus the customer's actual payments
        if new_doc:
            if return_total > 0:
                add_payment_to_doc(new_doc, default_mop, return_total)
            for p in customer_payments:
                amt = flt(p.get("amount", 0))
                mop = p.get("mode_of_payment")
                if not mop or (valid_mops and mop not in valid_mops):
                    mop = default_mop
                    p["mode_of_payment"] = default_mop
                add_payment_to_doc(new_doc, mop, amt)
            new_doc.paid_amount = sum(flt(pay.amount) for pay in new_doc.payments)

    else:
        # Customer gets a refund:
        # New invoice is settled entirely with default MOP
        if new_doc and new_total > 0:
            add_payment_to_doc(new_doc, default_mop, new_total)
            new_doc.paid_amount = new_total
            
        # Return invoice is settled with default MOP up to the new_total, plus the customer's refund payments
        if return_doc:
            if new_total > 0:
                add_payment_to_doc(return_doc, default_mop, -new_total)
            
            # If no customer payments were provided for the refund, auto-refund with default_mop
            if not customer_payments:
                customer_payments.append({"mode_of_payment": default_mop, "amount": difference})
                
            for p in customer_payments:
                amt = flt(p.get("amount", 0))
                # Note: customer_payments for refunds should be passed as negative amounts from frontend,
                # or if passed positive, we must negate it.
                if amt > 0:
                    amt = -amt 
                mop = p.get("mode_of_payment")
                if not mop or (valid_mops and mop not in valid_mops):
                    mop = default_mop
                    p["mode_of_payment"] = default_mop
                add_payment_to_doc(return_doc, mop, amt)
            return_doc.paid_amount = sum(flt(pay.amount) for pay in return_doc.payments)
