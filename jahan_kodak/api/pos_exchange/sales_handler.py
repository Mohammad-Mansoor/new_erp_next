import frappe

def create_replacement_invoice(original_invoice, new_items):
    """
    Creates and returns a draft POS Invoice for the replacement items.
    """
    if not new_items:
        return None
        
    new_doc = frappe.new_doc("POS Invoice")
    
    # Inherit context from the original invoice to ensure POS consistency
    new_doc.customer = original_invoice.customer
    new_doc.company = original_invoice.company
    new_doc.pos_profile = original_invoice.pos_profile
    new_doc.currency = original_invoice.currency
    new_doc.selling_price_list = original_invoice.selling_price_list
    new_doc.is_pos = 1
    new_doc.update_billed_amount_in_delivery_note = True
    new_doc.set_posting_time = 1
    
    for req_item in new_items:
        # Standard Frappe row initialization
        row = new_doc.append("items", {})
        row.item_code = req_item.get("item_code")
        row.qty = float(req_item.get("qty", 0))
        
        # Additional standard fields if provided by frontend
        if req_item.get("warehouse"):
            row.warehouse = req_item.get("warehouse")
        if req_item.get("serial_no"):
            row.serial_no = req_item.get("serial_no")
        if req_item.get("batch_no"):
            row.batch_no = req_item.get("batch_no")
            
    # Trigger standard ERPNext authoritative calculations
    # This fetches prices, taxes, pricing rules, and sets standard defaults
    new_doc.set_missing_values()
    new_doc.calculate_taxes_and_totals()
    
    return new_doc
