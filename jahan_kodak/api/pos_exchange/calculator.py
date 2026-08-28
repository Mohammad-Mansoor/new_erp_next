def calculate_exchange_difference(return_doc, new_doc):
    """
    Calculates the exact financial difference based on the authoritative
    ERPNext document totals (which already include taxes and discounts).
    
    return_doc.grand_total is negative.
    new_doc.grand_total is positive.
    
    Customer pays if new_doc total > abs(return_doc total)
    Customer gets refund if abs(return_doc total) > new_doc total
    """
    return_total = abs(return_doc.grand_total) if return_doc else 0.0
    new_total = new_doc.grand_total if new_doc else 0.0
    
    difference = new_total - return_total
    
    return return_total, new_total, difference
