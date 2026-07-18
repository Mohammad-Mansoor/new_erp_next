import frappe
from erpnext.controllers.item_variant import create_variant_doc_for_quick_entry
import json

def run():
    frappe.flags.in_test = True
    args = json.dumps({"Colour": "Red", "Size": "Extra Large"})
    try:
        result = create_variant_doc_for_quick_entry("5207", args)
        if isinstance(result, str):
            print("API returned string:", result)
        else:
            print("API returned item_code:", result.get("item_code"))
    except Exception as e:
        import traceback
        traceback.print_exc()
