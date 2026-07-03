import frappe

def run():
    frappe.flags.in_test = True
    company = "Jahan Kodak"
    
    # 1. Create Warehouses
    root_wh = "All Warehouses - JK"
    
    if not frappe.db.exists("Warehouse", root_wh):
        root_doc = frappe.get_doc({
            "doctype": "Warehouse",
            "warehouse_name": "All Warehouses",
            "company": company,
            "is_group": 1
        })
        root_doc.insert(ignore_permissions=True)

    def create_wh(name, is_group=0, parent=root_wh):
        wh_name = f"{name} - JK"
        if not frappe.db.exists("Warehouse", wh_name):
            doc = frappe.get_doc({
                "doctype": "Warehouse",
                "warehouse_name": name,
                "company": company,
                "parent_warehouse": parent,
                "is_group": is_group
            })
            doc.insert(ignore_permissions=True)
            print(f"Created WH: {wh_name}")

    create_wh("Central Warehouse", is_group=1)
    create_wh("Receiving Area")
    create_wh("In Transit")
    
    branches = ["Kabul Center", "Shahr-e-Naw", "Karteh Naw", "Macroyan", "Dasht-e-Barchi"]
    for b in branches:
        create_wh(b)
        
    # 2. Create Item Attributes
    attributes = {
        "Size": ["XS", "S", "M", "L", "XL", "XXL"],
        "Color": ["Black", "White", "Red", "Blue", "Navy"],
        "Brand": ["Jahan Kodak", "Nike", "Adidas"]
    }
    
    for attr, values in attributes.items():
        if not frappe.db.exists("Item Attribute", attr):
            doc = frappe.get_doc({
                "doctype": "Item Attribute",
                "attribute_name": attr,
                "item_attribute_values": [{"attribute_value": v, "abbr": v[:3].upper()} for v in values]
            })
            doc.insert(ignore_permissions=True)
            print(f"Created Item Attribute: {attr}")

    # 3. Server Script for SKU Generation
    script_name = "Generate SKU for Item"
    if not frappe.db.exists("Server Script", script_name):
        script = """
if doc.has_variants == 0 and doc.variant_of:
    template = frappe.get_doc("Item", doc.variant_of)
    group = frappe.db.get_value("Item Group", template.item_group, "name")[:3].upper() if template.item_group else "ITM"
    year = "2026"
    color = "N/A"
    size = "N/A"
    if hasattr(doc, 'attributes'):
        for attr in doc.attributes:
            if attr.attribute == "Color":
                val = frappe.db.get_value("Item Attribute Value", {"parent": "Color", "attribute_value": attr.attribute_value}, "abbr")
                color = val if val else attr.attribute_value[:3].upper()
            if attr.attribute == "Size":
                val = frappe.db.get_value("Item Attribute Value", {"parent": "Size", "attribute_value": attr.attribute_value}, "abbr")
                size = val if val else attr.attribute_value[:3].upper()
                
    doc.item_code = f"{group}-{year}-{color}-{size}"
    doc.item_name = doc.item_code
"""
        doc = frappe.get_doc({
            "doctype": "Server Script",
            "name": script_name,
            "script_type": "DocType Event",
            "reference_doctype": "Item",
            "doctype_event": "Before Validate",
            "script": script
        })
        try:
            doc.insert(ignore_permissions=True)
            print("Created Server Script for SKU Generation")
        except Exception as e:
            print("Could not create server script. Error:", e)

    # 4. Workflow for Branch Replenishment
    workflow_name = "Branch Replenishment"
    if not frappe.db.exists("Workflow", workflow_name):
        states = ["Pending Request", "Warehouse Approved", "In Transit", "Received"]
        for s in states:
            if not frappe.db.exists("Workflow State", s):
                frappe.get_doc({"doctype": "Workflow State", "workflow_state_name": s}).insert(ignore_permissions=True)
                
        actions = ["Approve Transfer", "Dispatch to Transit", "Receive at Branch"]
        for a in actions:
            if not frappe.db.exists("Workflow Action Master", a):
                frappe.get_doc({"doctype": "Workflow Action Master", "workflow_action_name": a}).insert(ignore_permissions=True)
                
        doc = frappe.get_doc({
            "doctype": "Workflow",
            "workflow_name": workflow_name,
            "document_type": "Material Request",
            "is_active": 1,
            "states": [
                {"state": "Pending Request", "doc_status": 0, "allow_edit": "System Manager"},
                {"state": "Warehouse Approved", "doc_status": 1, "allow_edit": "System Manager"},
                {"state": "In Transit", "doc_status": 1, "allow_edit": "System Manager"},
                {"state": "Received", "doc_status": 1, "allow_edit": "System Manager"}
            ],
            "transitions": [
                {"state": "Pending Request", "action": "Approve Transfer", "next_state": "Warehouse Approved", "allowed": "System Manager"},
                {"state": "Warehouse Approved", "action": "Dispatch to Transit", "next_state": "In Transit", "allowed": "System Manager"},
                {"state": "In Transit", "action": "Receive at Branch", "next_state": "Received", "allowed": "System Manager"}
            ]
        })
        doc.insert(ignore_permissions=True)
        print("Created Workflow: Branch Replenishment")

    frappe.db.commit()
    print("Phase 3 Execution Completed.")
