import frappe

def run():
    script = frappe.get_doc("Server Script", "Generate SKU for Item")
    new_code = """
if doc.has_variants == 0 and doc.variant_of:
    template = frappe.get_doc("Item", doc.variant_of)
    group = frappe.db.get_value("Item Group", template.item_group, "name")[:3].upper() if template.item_group else "ITM"
    
    attr_abbrs = []
    if doc.get('attributes'):
        for attr in doc.attributes:
            # We must fetch the custom field from the TEMPLATE's attributes, 
            # because Frappe does not copy custom child table fields to the variant memory!
            is_included = False
            for t_attr in template.attributes:
                if t_attr.attribute == attr.attribute:
                    is_included = t_attr.get("custom_include_in_sku")
                    break
                    
            if is_included:
                val = frappe.db.get_value("Item Attribute Value", {"parent": attr.attribute, "attribute_value": attr.attribute_value}, "abbr")
                if not val:
                    val = str(attr.attribute_value)[:3].upper() if attr.attribute_value else "XXX"
                attr_abbrs.append(val)
                
    # Build Prefix
    base_sku = f"{group}-" + "-".join(attr_abbrs) + "-" if attr_abbrs else f"{group}-"
    
    # Auto-Increment Logic (001, 002)
    existing_items = frappe.db.get_all("Item", filters={"item_code": ("like", base_sku + "%")}, fields=["item_code"])
    
    max_num = 0
    for item in existing_items:
        code = item.item_code
        if code.startswith(base_sku):
            num_str = code[len(base_sku):]
            if num_str.isdigit():
                max_num = max(max_num, int(num_str))
                
    next_num = max_num + 1
    sku = f"{base_sku}{next_num:03d}"
    
    # Set SKU and NAME
    doc.item_code = sku
    doc.item_name = doc.item_code
    doc.name = sku
    
    # Auto-generate Barcode
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
    script.script = new_code
    script.disabled = 0
    script.save()
    frappe.db.commit()
    print("Successfully restored Server Script with template attribute check")
