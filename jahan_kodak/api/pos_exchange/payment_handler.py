import frappe

def get_default_mop(pos_profile):
    """
    Retrieves the default Mode of Payment for the POS Profile.
    """
    default_mop = frappe.db.get_value("POS Profile", pos_profile, "write_off_account") # Wait, POS Payment method has a default flag.
    
    mops = frappe.get_all(
        "POS Payment Method",
        filters={"parent": pos_profile},
        fields=["mode_of_payment", "default"]
    )
    
    if not mops:
        frappe.throw(_("No Mode of Payment configured for POS Profile {0}").format(pos_profile))
        
    for mop in mops:
        if mop.default:
            return mop.mode_of_payment
            
    return mops[0].mode_of_payment

def apply_settlement(return_doc, new_doc, difference, customer_payments):
    """
    Settles both invoices using standard ERPNext accounting.
    
    We use the default Mode of Payment for the 'internal' clearing of the exchange,
    and apply the actual customer payments (or refunds) to handle the difference.
    """
    pos_profile = return_doc.pos_profile if return_doc else (new_doc.pos_profile if new_doc else None)
    if not pos_profile:
        return
        
    default_mop = get_default_mop(pos_profile)
    
    # 1. Clear out the original payments from return_doc that make_return_doc might have copied
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
        if return_doc:
            return_doc.append("payments", {"mode_of_payment": default_mop, "amount": -return_total})
            return_doc.paid_amount = -return_total
        if new_doc:
            new_doc.append("payments", {"mode_of_payment": default_mop, "amount": new_total})
            new_doc.paid_amount = new_total
            
    elif difference > 0:
        # Customer pays:
        # Return invoice is settled entirely with default MOP
        if return_doc:
            return_doc.append("payments", {"mode_of_payment": default_mop, "amount": -return_total})
            return_doc.paid_amount = -return_total
            
        # New invoice is settled with default MOP up to the return_total, plus the customer's actual payments
        if new_doc:
            new_doc.append("payments", {"mode_of_payment": default_mop, "amount": return_total})
            paid = return_total
            for p in customer_payments:
                amt = float(p.get("amount", 0))
                new_doc.append("payments", {"mode_of_payment": p.get("mode_of_payment"), "amount": amt})
                paid += amt
            new_doc.paid_amount = paid

    else:
        # Customer gets a refund:
        # New invoice is settled entirely with default MOP
        if new_doc:
            new_doc.append("payments", {"mode_of_payment": default_mop, "amount": new_total})
            new_doc.paid_amount = new_total
            
        # Return invoice is settled with default MOP up to the new_total, plus the customer's refund payments
        if return_doc:
            return_doc.append("payments", {"mode_of_payment": default_mop, "amount": -new_total})
            paid = -new_total
            for p in customer_payments:
                amt = float(p.get("amount", 0))
                # Note: customer_payments for refunds should be passed as negative amounts from frontend,
                # or if passed positive, we must negate it.
                if amt > 0: amt = -amt 
                return_doc.append("payments", {"mode_of_payment": p.get("mode_of_payment"), "amount": amt})
                paid += amt
            return_doc.paid_amount = paid
