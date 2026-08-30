import frappe
def test():
    frappe.init(site="development.localhost")
    frappe.connect()
    invoices = frappe.db.sql("""
        SELECT parent FROM `tabPOS Invoice Item` 
        WHERE item_code = 'PRO-2026-MENS-ML-JAH-XL-WHI' AND docstatus = 1
    """, as_dict=True)
    print("Invoices with out of stock item:", invoices)
test()
