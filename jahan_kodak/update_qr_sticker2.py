import frappe

def update():
    pf_name = "Item QR Sticker"
    if frappe.db.exists("Print Format", pf_name):
        doc = frappe.get_doc("Print Format", pf_name)
        if doc.html:
            # Replace Item Name style back to normal without !important
            doc.html = doc.html.replace(
                "font-weight: bold !important; color: black !important;",
                "font-weight: bold; color: black;"
            )
            
            doc.save(ignore_permissions=True)
            frappe.db.commit()
            print("Successfully updated Item QR Sticker in database.")
        else:
            print("No HTML found in Print Format.")
    else:
        print("Print Format not found.")
