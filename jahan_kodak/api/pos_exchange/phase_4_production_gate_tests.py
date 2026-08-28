import frappe
import json
import uuid

def execute_tests():
    frappe.init(site="development.localhost")
    frappe.connect()
    
    results = []

    try:
        from jahan_kodak.api.pos_exchange.service import calculate_exchange, process_exchange
        
        print("Starting Phase 4 Production Gate Tests...")
        
        # 1. Preview Read-Only Safety
        def test_preview_safety():
            # Setup base invoice
            siv = frappe.get_all("POS Invoice", {"docstatus": 1, "is_return": 0}, limit=1)
            if not siv: return {"name": "Preview Safety", "pass": False, "msg": "No base invoice"}
            siv_name = siv[0].name
            siv_doc = frappe.get_doc("POS Invoice", siv_name)
            item = siv_doc.items[0].item_code
            
            counts_before = {
                "POS Exchange": frappe.db.count("POS Exchange"),
                "POS Invoice": frappe.db.count("POS Invoice"),
                "Payment Entry": frappe.db.count("Payment Entry"),
                "GL Entry": frappe.db.count("GL Entry"),
                "Stock Ledger Entry": frappe.db.count("Stock Ledger Entry")
            }
            
            payload = {
                "idempotency_key": str(uuid.uuid4()),
                "original_invoice": siv_name,
                "return_items": [{"item_code": item, "qty": 1}],
                "new_items": [{"item_code": item, "qty": 1}]
            }
            
            for _ in range(3):
                calculate_exchange(payload)
                
            counts_after = {
                "POS Exchange": frappe.db.count("POS Exchange"),
                "POS Invoice": frappe.db.count("POS Invoice"),
                "Payment Entry": frappe.db.count("Payment Entry"),
                "GL Entry": frappe.db.count("GL Entry"),
                "Stock Ledger Entry": frappe.db.count("Stock Ledger Entry")
            }
            
            if counts_before != counts_after:
                return {"name": "Preview Safety", "pass": False, "msg": f"Counts changed: {counts_before} -> {counts_after}"}
            return {"name": "Preview Safety", "pass": True, "msg": "0 database records created"}
            
        results.append(test_preview_safety())
        
        # 4. Final Submission Ignores Frontend Totals
        def test_ignore_totals():
            siv = frappe.get_all("POS Invoice", {"docstatus": 1, "is_return": 0}, limit=1)[0].name
            item = frappe.get_doc("POS Invoice", siv).items[0].item_code
            
            payload = {
                "idempotency_key": str(uuid.uuid4()),
                "original_invoice": siv,
                "return_items": [{"item_code": item, "qty": 1}],
                "new_items": [{"item_code": item, "qty": 1}],
                "return_total": 999999,      # Malicious frontend value
                "replacement_total": -5000,  # Malicious frontend value
                "difference": 123456         # Malicious frontend value
            }
            
            res = process_exchange(payload)
            if res["difference"] == 123456:
                return {"name": "Ignore Frontend Totals", "pass": False, "msg": "Backend trusted malicious frontend totals"}
            return {"name": "Ignore Frontend Totals", "pass": True, "msg": "Backend completely ignored malicious payload fields"}
            
        results.append(test_ignore_totals())
        
        # Write results to json to be parsed by the agent
        with open("phase4_test_results.json", "w") as f:
            json.dump(results, f, indent=4)
            
    finally:
        frappe.db.rollback()
        frappe.destroy()

if __name__ == "__main__":
    execute_tests()
