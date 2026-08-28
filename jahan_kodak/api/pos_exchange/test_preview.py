import frappe
import json

def test_preview_safety():
    print("Testing Preview Safety...")
    
    # Get initial counts
    counts = {
        "POS Exchange": frappe.db.count("POS Exchange"),
        "POS Invoice": frappe.db.count("POS Invoice"),
        "Payment Entry": frappe.db.count("Payment Entry"),
        "GL Entry": frappe.db.count("GL Entry"),
        "Stock Ledger Entry": frappe.db.count("Stock Ledger Entry")
    }
    
    # We need a submitted POS Invoice to test against
    siv = frappe.db.get_value("POS Invoice", {"docstatus": 1, "is_return": 0}, "name")
    if not siv:
        print("No submitted POS Invoice found. Please create one first.")
        return
        
    siv_doc = frappe.get_doc("POS Invoice", siv)
    item = siv_doc.items[0]
    
    payload = {
        "original_invoice": siv,
        "return_items": [{"item_code": item.item_code, "qty": 1}],
        "new_items": [{"item_code": item.item_code, "qty": 1}]
    }
    
    from jahan_kodak.api.pos_exchange.service import calculate_exchange
    
    # Run preview multiple times
    for _ in range(3):
        res = calculate_exchange(payload)
        assert res.get("difference") == 0
        
    # Check counts again
    new_counts = {
        "POS Exchange": frappe.db.count("POS Exchange"),
        "POS Invoice": frappe.db.count("POS Invoice"),
        "Payment Entry": frappe.db.count("Payment Entry"),
        "GL Entry": frappe.db.count("GL Entry"),
        "Stock Ledger Entry": frappe.db.count("Stock Ledger Entry")
    }
    
    for doctype in counts:
        if counts[doctype] != new_counts[doctype]:
            print(f"FAILED: {doctype} count changed from {counts[doctype]} to {new_counts[doctype]}")
            return
            
    print("SUCCESS: Preview database safety verified. No records were created.")
    
def test_consistency():
    print("Testing Preview/Submission Consistency...")
    siv = frappe.db.get_value("POS Invoice", {"docstatus": 1, "is_return": 0}, "name")
    if not siv:
        print("No submitted POS Invoice found.")
        return
        
    siv_doc = frappe.get_doc("POS Invoice", siv)
    item = siv_doc.items[0]
    
    import uuid
    idempotency_key = str(uuid.uuid4())
    
    payload = {
        "idempotency_key": idempotency_key,
        "original_invoice": siv,
        "return_items": [{"item_code": item.item_code, "qty": 1}],
        "new_items": [{"item_code": item.item_code, "qty": 1}]
    }
    
    from jahan_kodak.api.pos_exchange.service import calculate_exchange, process_exchange
    
    # 1. Preview
    preview_res = calculate_exchange(payload)
    
    # 2. Process
    process_res = process_exchange(payload)
    
    if abs(preview_res["difference"] - process_res["difference"]) > 0.001:
        print(f"FAILED: Consistency mismatch. Preview Diff = {preview_res['difference']}, Process Diff = {process_res['difference']}")
        return
        
    print("SUCCESS: Preview and Submission consistency verified.")

def main():
    frappe.init(site="development.localhost")
    frappe.connect()
    
    try:
        test_preview_safety()
        test_consistency()
    finally:
        frappe.destroy()

if __name__ == "__main__":
    main()
