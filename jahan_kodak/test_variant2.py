import frappe

def run():
    from erpnext.controllers.item_variant import create_variant
    
    frappe.flags.in_test = True
    args = {"Colour": "Blue", "Size": "XXL"}
    variant = create_variant("5207", args)
    variant.save()
    print("Created Variant Name:", variant.name)
    frappe.db.rollback()
