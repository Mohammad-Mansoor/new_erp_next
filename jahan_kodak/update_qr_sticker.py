import frappe

def update():
    pf_name = "Item QR Sticker"
    if frappe.db.exists("Print Format", pf_name):
        doc = frappe.get_doc("Print Format", pf_name)
        if doc.html:
            # Replace Item Name style
            doc.html = doc.html.replace(
                "font-size: 10px; font-weight: 600; color: #333333;",
                "font-size: 10px; font-weight: bold !important; color: black !important;"
            )
            # Replace Price style
            doc.html = doc.html.replace(
                "font-size: 12px; font-weight: 900; color: #000000;",
                "font-size: 12px; font-weight: bold !important; color: black !important;"
            )
            doc.save(ignore_permissions=True)
            frappe.db.commit()
            print("Successfully updated Item QR Sticker in database.")
        else:
            print("No HTML found in Print Format.")
    else:
        print("Print Format not found.")
