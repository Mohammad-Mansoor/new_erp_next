import frappe

def make_custom_variant_item_code(template_item_code, template_item_name, variant):
    """Overrides erpnext's standard make_variant_item_code to use our custom SKU format"""
    if variant.item_code:
        return

    group = "ITM"
    template = None
    if variant.variant_of:
        template = frappe.get_doc("Item", variant.variant_of)
        if template.item_group:
            group = frappe.db.get_value("Item Group", template.item_group, "name")[:3].upper()
            
    attr_abbrs = []
    if variant.get('attributes'):
        for attr in variant.attributes:
            is_included = False
            if template:
                for t_attr in template.attributes:
                    if t_attr.attribute == attr.attribute:
                        is_included = t_attr.get("custom_include_in_sku")
                        break
                        
            if is_included:
                val = frappe.db.get_value("Item Attribute Value", {"parent": attr.attribute, "attribute_value": attr.attribute_value}, "abbr")
                if not val:
                    val = str(attr.attribute_value)[:3].upper() if attr.attribute_value else "XXX"
                attr_abbrs.append(val)
                
    base_sku = f"{group}-" + "-".join(attr_abbrs) + "-" if attr_abbrs else f"{group}-"
    
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
    
    variant.item_code = sku
    variant.item_name = sku

def apply_patch():
    import erpnext.controllers.item_variant
    import erpnext.stock.doctype.item.item
    
    erpnext.controllers.item_variant.make_variant_item_code = make_custom_variant_item_code
    erpnext.stock.doctype.item.item.make_variant_item_code = make_custom_variant_item_code
