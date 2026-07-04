import frappe

def run():
    script = """
if doc.has_variants == 0 and doc.variant_of:
    template = frappe.get_doc("Item", doc.variant_of)
    group = frappe.db.get_value("Item Group", template.item_group, "name")[:3].upper() if template.item_group else "ITM"
    year = "2026"
    
    attr_abbrs = []
    if doc.get('attributes'):
        for attr in doc.attributes:
            val = frappe.db.get_value("Item Attribute Value", {"parent": attr.attribute, "attribute_value": attr.attribute_value}, "abbr")
            if not val:
                val = str(attr.attribute_value)[:3].upper() if attr.attribute_value else "XXX"
            attr_abbrs.append(val)
            
    # Set SKU
    doc.item_code = f"{group}-{year}-" + "-".join(attr_abbrs)
    doc.item_name = doc.item_code
    
    # Auto-generate Barcode (identical to SKU)
    barcode_exists = False
    if doc.get("barcodes"):
        for b in doc.barcodes:
            if b.barcode == doc.item_code:
                barcode_exists = True
                break
                
    if not barcode_exists:
        doc.append("barcodes", {
            "barcode": doc.item_code
        })
"""

    doc = frappe.get_doc('Server Script', 'Generate SKU for Item')
    doc.script = script
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Server script updated successfully to include Barcode generation!")
