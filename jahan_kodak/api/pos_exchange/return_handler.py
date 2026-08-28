import frappe
from erpnext.controllers.sales_and_purchase_return import make_return_doc

def create_return_invoice(original_invoice, return_items):
    """
    Creates and returns a draft POS Return Invoice based on the specified returned items.
    """
    # Create the standard return document in memory
    return_doc = make_return_doc("POS Invoice", original_invoice.name)
    
    # Map the return request for easy lookup
    # Because there can be multiple rows with the same item, we need to match carefully,
    # or just use item_code as primary if they don't split rows.
    # To be safe, we'll build a required quantity map
    req_qty_map = {}
    req_serial_nos = {}
    for r in return_items:
        ic = r.get("item_code")
        req_qty_map[ic] = req_qty_map.get(ic, 0) + float(r.get("qty", 0))
        if r.get("serial_no"):
            req_serial_nos.setdefault(ic, []).append(r.get("serial_no"))
            
    # Iterate over the return_doc items (which currently hold full negative quantities)
    # and adjust them down to the requested return quantities, removing unreturned items.
    final_items = []
    
    for item in return_doc.items:
        if item.item_code in req_qty_map and req_qty_map[item.item_code] > 0:
            max_row_returnable = abs(item.qty)
            qty_to_return_from_this_row = min(max_row_returnable, req_qty_map[item.item_code])
            
            # Reduce required quantity
            req_qty_map[item.item_code] -= qty_to_return_from_this_row
            
            # Set the exact negative quantity for this row
            item.qty = -1 * qty_to_return_from_this_row
            
            # Handle serial numbers if any
            if item.serial_no and req_serial_nos.get(item.item_code):
                # The frontend should pass the exact serial_nos being returned.
                # We need to filter item.serial_no down to only those returned.
                original_serials = [s.strip() for s in item.serial_no.split('\n') if s.strip()]
                returned_serials = []
                for s in list(req_serial_nos[item.item_code]):
                    if s in original_serials:
                        returned_serials.append(s)
                        req_serial_nos[item.item_code].remove(s)
                item.serial_no = '\n'.join(returned_serials)
                
            final_items.append(item)
            
    return_doc.items = final_items
    
    # Calculate taxes and totals based on the new reduced quantities
    return_doc.set_missing_values()
    return_doc.calculate_taxes_and_totals()
    
    return return_doc
