import frappe
from frappe.utils import flt

@frappe.whitelist()
def get_item_selling_rate(item_code, price_list=None):
    """
    Fetch the current selling price of an item from Item Price for the specified price list,
    or fall back to standard_rate on the Item master.
    """
    if not item_code:
        return 0

    if not price_list:
        price_list = (
            frappe.db.get_single_value("Selling Settings", "selling_price_list")
            or "Standard Selling"
        )

    rate = frappe.db.get_value(
        "Item Price",
        {"item_code": item_code, "price_list": price_list, "selling": 1},
        "price_list_rate"
    )
    if rate:
        return flt(rate)

    # Fallback to Item.standard_rate
    standard_rate = frappe.db.get_value("Item", item_code, "standard_rate")
    return flt(standard_rate) or 0


def update_selling_rates(doc, method=None):
    """
    Hooked on Purchase Receipt on_submit.
    Updates or creates Item Price records for the chosen selling price list and Item.standard_rate
    for each item where custom_selling_rate is specified.
    """
    target_price_list = (
        doc.get("custom_selling_price_list")
        or frappe.db.get_single_value("Selling Settings", "selling_price_list")
        or "Standard Selling"
    )
    updated_items = []

    for row in doc.get("items", []):
        selling_rate = getattr(row, "custom_selling_rate", None)
        if selling_rate is None and hasattr(row, "get"):
            selling_rate = row.get("custom_selling_rate")

        if not selling_rate or flt(selling_rate) <= 0:
            continue

        item_code = getattr(row, "item_code", None)
        if not item_code and hasattr(row, "get"):
            item_code = row.get("item_code")

        new_rate = flt(selling_rate)

        # 1. Update or create Item Price record for target_price_list
        item_price_name = frappe.db.get_value(
            "Item Price",
            {"item_code": item_code, "price_list": target_price_list, "selling": 1},
            "name"
        )

        if item_price_name:
            frappe.db.set_value("Item Price", item_price_name, "price_list_rate", new_rate)
        else:
            currency = (
                doc.currency
                or frappe.get_cached_value("Company", doc.company, "default_currency")
                or "AFN"
            )
            ip = frappe.get_doc({
                "doctype": "Item Price",
                "item_code": item_code,
                "price_list": target_price_list,
                "price_list_rate": new_rate,
                "selling": 1,
                "currency": currency
            })
            ip.insert(ignore_permissions=True)

        # 2. Update standard_rate on the Item master
        frappe.db.set_value("Item", item_code, "standard_rate", new_rate)
        updated_items.append(f"{item_code}: {new_rate}")

    if updated_items:
        doc.add_comment(
            "Comment",
            f"Updated Selling Rates in {target_price_list}: {', '.join(updated_items)}"
        )


def setup_custom_fields():
    """
    Ensure the custom fields exist on Purchase Receipt and Purchase Receipt Item.
    Can be run via bench execute or install/migrate hooks.
    """
    from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
    custom_fields = {
        "Purchase Receipt": [
            {
                "fieldname": "custom_selling_price_list",
                "label": "Selling Price List",
                "fieldtype": "Link",
                "options": "Price List",
                "default": "Standard Selling",
                "insert_after": "buying_price_list",
                "module": "Jahan Kodak",
                "description": "Selling Price List to update with items' selling rates upon submission"
            }
        ],
        "Purchase Receipt Item": [
            {
                "fieldname": "custom_selling_rate",
                "label": "Selling Rate",
                "fieldtype": "Currency",
                "options": "Company:company:default_currency",
                "insert_after": "rate",
                "in_list_view": 1,
                "module": "Jahan Kodak",
                "description": "Selling rate to be updated in Item Price on submission"
            }
        ]
    }
    create_custom_fields(custom_fields, update=True)
    frappe.db.commit()
    print("Successfully created/updated custom fields on Purchase Receipt and Purchase Receipt Item.")
