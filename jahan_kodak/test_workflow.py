import frappe

def test():
    frappe.set_user("Administrator")
    doc = frappe.get_doc("Stock Settings")
    doc.allow_negative_stock = 1
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Enabled Allow Negative Stock!")

