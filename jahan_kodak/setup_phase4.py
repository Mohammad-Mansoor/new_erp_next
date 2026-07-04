import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def run():
    frappe.flags.in_test = True
    
    # 1. Update/Replace Workflow for Material Request
    # Deactivate old workflow to avoid conflicts
    if frappe.db.exists("Workflow", "Branch Replenishment"):
        old_wf = frappe.get_doc("Workflow", "Branch Replenishment")
        old_wf.is_active = 0
        old_wf.save(ignore_permissions=True)
        
    wf_name = "JK Material Request Flow"
    if not frappe.db.exists("Workflow", wf_name):
        states = ["Pending", "Branch Manager Approved", "Procurement Approved", "Warehouse Approved", "In Transit", "Received"]
        for s in states:
            if not frappe.db.exists("Workflow State", s):
                frappe.get_doc({"doctype": "Workflow State", "workflow_state_name": s}).insert(ignore_permissions=True)
                
        actions = ["Approve Transfer", "Dispatch to Transit", "Receive at Branch", "BM Approve", "Procurement Approve", "Reject"]
        for a in actions:
            if not frappe.db.exists("Workflow Action Master", a):
                frappe.get_doc({"doctype": "Workflow Action Master", "workflow_action_name": a}).insert(ignore_permissions=True)
                
        doc = frappe.get_doc({
            "doctype": "Workflow",
            "workflow_name": wf_name,
            "document_type": "Material Request",
            "is_active": 1,
            "states": [
                {"state": "Pending", "doc_status": 0, "allow_edit": "System Manager"},
                {"state": "Branch Manager Approved", "doc_status": 0, "allow_edit": "System Manager"},
                {"state": "Procurement Approved", "doc_status": 1, "allow_edit": "System Manager"},
                {"state": "Warehouse Approved", "doc_status": 1, "allow_edit": "System Manager"},
                {"state": "In Transit", "doc_status": 1, "allow_edit": "System Manager"},
                {"state": "Received", "doc_status": 1, "allow_edit": "System Manager"}
            ],
            "transitions": [
                # Purchase Flow
                {"state": "Pending", "action": "BM Approve", "next_state": "Branch Manager Approved", "allowed": "System Manager", "condition": "doc.material_request_type == 'Purchase'"},
                {"state": "Branch Manager Approved", "action": "Procurement Approve", "next_state": "Procurement Approved", "allowed": "System Manager", "condition": "doc.material_request_type == 'Purchase'"},
                
                # Transfer Flow
                {"state": "Pending", "action": "Approve Transfer", "next_state": "Warehouse Approved", "allowed": "System Manager", "condition": "doc.material_request_type == 'Material Transfer'"},
                {"state": "Warehouse Approved", "action": "Dispatch to Transit", "next_state": "In Transit", "allowed": "System Manager", "condition": "doc.material_request_type == 'Material Transfer'"},
                {"state": "In Transit", "action": "Receive at Branch", "next_state": "Received", "allowed": "System Manager", "condition": "doc.material_request_type == 'Material Transfer'"}
            ]
        })
        doc.insert(ignore_permissions=True)
        print("Created flexible unified Workflow for Material Request")

    # 2. Add Custom Fields for Cargo Tracking to Purchase Order
    custom_fields = [
        {"dt": "Purchase Order", "fieldname": "cargo_company", "fieldtype": "Data", "label": "Cargo Company", "insert_after": "supplier"},
        {"dt": "Purchase Order", "fieldname": "cargo_tracking_number", "fieldtype": "Data", "label": "Cargo Tracking Number", "insert_after": "cargo_company"},
        {"dt": "Purchase Order", "fieldname": "expected_arrival_date", "fieldtype": "Date", "label": "Expected Arrival Date", "insert_after": "cargo_tracking_number"}
    ]
    
    for cf in custom_fields:
        if not frappe.db.exists("Custom Field", {"dt": cf["dt"], "fieldname": cf["fieldname"]}):
            create_custom_field(cf["dt"], cf)
            print(f"Created Custom Field: {cf['fieldname']}")

    frappe.db.commit()
    print("Phase 4 Execution Completed.")
