import frappe

def run():
    frappe.flags.in_test = True
    
    # 1. Create Item Groups for Manufacturing
    item_groups = ["Raw Materials - JK", "Finished Goods - JK"]
    for ig in item_groups:
        if not frappe.db.exists("Item Group", ig):
            doc = frappe.get_doc({
                "doctype": "Item Group",
                "item_group_name": ig,
                "parent_item_group": "All Item Groups",
                "is_group": 0
            })
            doc.insert(ignore_permissions=True)
            print(f"Created Item Group: {ig}")

    # 2. Create Manufacturing Operations
    operations = ["Cutting", "Sewing", "Quality Check", "Packaging"]
    for op in operations:
        if not frappe.db.exists("Operation", op):
            doc = frappe.get_doc({
                "doctype": "Operation",
                "name": op,
                "description": f"Standard {op} operation for Jahan Kodak garments."
            })
            doc.insert(ignore_permissions=True)
            print(f"Created Operation: {op}")

    # Workstation for Operations (Required in ERPNext)
    workstations = ["Cutting Room", "Sewing Floor", "QC Desk", "Packaging Station"]
    for ws in workstations:
        if not frappe.db.exists("Workstation", ws):
            doc = frappe.get_doc({
                "doctype": "Workstation",
                "workstation_name": ws,
                "description": f"{ws} for Jahan Kodak production."
            })
            doc.insert(ignore_permissions=True)
            print(f"Created Workstation: {ws}")

    frappe.db.commit()
    print("Phase 5 Manufacturing Infrastructure Execution Completed.")
