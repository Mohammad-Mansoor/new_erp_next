import frappe
from erpnext.selling.page.point_of_sale.point_of_sale import get_items

def run():
    try:
        res = get_items(
            start=0,
            page_length=1,
            price_list="Standard Selling",
            item_group="",
            pos_profile="Default POS Profile",
            search_term=""
        )
        print("SUCCESS")
    except Exception as e:
        import traceback
        traceback.print_exc()
