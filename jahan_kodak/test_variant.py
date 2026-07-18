import frappe

def run():
    frappe.flags.in_test = True
    template = frappe.get_doc("Item", "5207")
    variant = frappe.new_doc("Item")
    variant.item_code = "TEST-VARIANT-001"
    variant.item_group = "Products"
    variant.variant_of = "5207"
    variant.has_variants = 0
    variant.append("attributes", {
        "attribute": "Color",
        "attribute_value": "Black"
    })
    variant.append("attributes", {
        "attribute": "Size",
        "attribute_value": "L"
    })
    variant.flags.ignore_mandatory = True
    variant.insert()
    print("Inserted variant. Name:", variant.name, "Item Code:", variant.item_code)
    frappe.db.rollback()
