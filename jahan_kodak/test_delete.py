import frappe

def test():
    frappe.set_user("Administrator")
    try:
        frappe.delete_doc("POS Closing Entry", "POS-CLO-2026-00030", force=1)
        frappe.db.commit()
        print("Successfully deleted!")
    except Exception as e:
        import traceback
        traceback.print_exc()
