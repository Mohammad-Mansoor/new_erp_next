import os
import glob
import frappe

@frappe.whitelist()
def print_item_label(item_code, qty=1):
    try:
        qty = int(qty) if qty else 1
    except ValueError:
        qty = 1

    doc = frappe.get_doc("Item", item_code)
    
    # Fetch barcode value
    barcode_val = doc.item_code
    if hasattr(doc, "barcodes") and doc.barcodes and len(doc.barcodes) > 0:
        if doc.barcodes[0].barcode:
            barcode_val = doc.barcodes[0].barcode
    elif getattr(doc, "barcode", None):
        barcode_val = doc.barcode

    # Fetch selling price
    price_val = frappe.db.get_value("Item Price", {"item_code": doc.name, "selling": 1}, "price_list_rate") or doc.standard_rate or doc.last_purchase_rate or 0.0
    price_str = f"AFN {price_val:,.2f}"

    # Build TSPL hardware commands
    tspl = f"""SIZE 50 mm, 30 mm\r
GAP 3 mm, 0 mm\r
CLS\r
TEXT 10,20,"2",0,1,1,"{doc.item_code[:25]}"\r
TEXT 10,38,"2",0,1,1,"{doc.item_name[:25]}"\r
BARCODE 10,60,"128M",40,0,0,1,1,"{barcode_val}"\r
TEXT 10,115,"3",0,1,1,"Price: {price_str}"\r
PRINT {qty},1\r
"""

    # Auto-detect label printer port
    ports = glob.glob("/dev/usb/lp*")
    if not ports:
        frappe.throw("No USB printer port found. Please check USB cable connection.")

    printed = False
    last_err = ""
    for port in reversed(sorted(ports)):
        try:
            with open(port, "wb") as f:
                f.write(tspl.encode("utf-8"))
            printed = True
            break
        except Exception as e:
            last_err = str(e)
            continue

    if not printed:
        frappe.throw(f"Failed to write to label printer port: {last_err}")

    return f"Successfully printed {qty} barcode label(s) for {doc.name}"
