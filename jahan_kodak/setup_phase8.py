import frappe

def run():
    frappe.init(site="development.localhost")
    frappe.connect()

    company = "Jahan Kodak"
    print("--- Starting Phase 8 Setup ---")

    # 1. Ensure Roles
    for role_name in ["Finance Manager", "Branch Manager", "Accounts User"]:
        if not frappe.db.exists("Role", role_name):
            doc = frappe.get_doc({
                "doctype": "Role",
                "role_name": role_name,
                "desk_access": 1
            })
            doc.insert(ignore_permissions=True)
            print(f"Created Role: {role_name}")

    # 2. Ensure Workflow States & Actions
    states = [
        "Draft", "Pending Finance Review", "Finance Manager Approved",
        "Rejected", "Pending Branch Manager Approval", "Approved"
    ]
    for st in states:
        if not frappe.db.exists("Workflow State", st):
            doc = frappe.get_doc({
                "doctype": "Workflow State",
                "workflow_state_name": st,
                "style": "Primary" if "Approved" in st else "Warning" if "Pending" in st else "Danger" if "Rejected" in st else "Inverse"
            })
            doc.insert(ignore_permissions=True)
            print(f"Created Workflow State: {st}")

    actions = [
        "Submit for Finance Review", "Approve Purchase Invoice", "Reject",
        "Submit for Branch Approval", "Approve POS Closing"
    ]
    for act in actions:
        if not frappe.db.exists("Workflow Action Master", act):
            doc = frappe.get_doc({
                "doctype": "Workflow Action Master",
                "workflow_action_name": act
            })
            doc.insert(ignore_permissions=True)
            print(f"Created Workflow Action Master: {act}")

    # 3. Task 8.2: Purchase Invoice Finance Approval Workflow
    pi_workflow_name = "Purchase Invoice Finance Approval"
    if frappe.db.exists("Workflow", pi_workflow_name):
        frappe.delete_doc("Workflow", pi_workflow_name, force=True)
        print(f"Removed existing Workflow: {pi_workflow_name}")

    pi_wf = frappe.get_doc({
        "doctype": "Workflow",
        "workflow_name": pi_workflow_name,
        "document_type": "Purchase Invoice",
        "is_active": 1,
        "override_status": 0,
        "workflow_state_field": "workflow_state",
        "states": [
            {
                "state": "Draft",
                "doc_status": "0",
                "allow_edit": "Accounts User"
            },
            {
                "state": "Pending Finance Review",
                "doc_status": "0",
                "allow_edit": "Finance Manager"
            },
            {
                "state": "Finance Manager Approved",
                "doc_status": "1",
                "allow_edit": "System Manager"
            },
            {
                "state": "Rejected",
                "doc_status": "0",
                "allow_edit": "Accounts User"
            }
        ],
        "transitions": [
            {
                "state": "Draft",
                "action": "Submit for Finance Review",
                "next_state": "Pending Finance Review",
                "allowed": "Accounts User"
            },
            {
                "state": "Draft",
                "action": "Submit for Finance Review",
                "next_state": "Pending Finance Review",
                "allowed": "System Manager"
            },
            {
                "state": "Pending Finance Review",
                "action": "Approve Purchase Invoice",
                "next_state": "Finance Manager Approved",
                "allowed": "Finance Manager"
            },
            {
                "state": "Pending Finance Review",
                "action": "Approve Purchase Invoice",
                "next_state": "Finance Manager Approved",
                "allowed": "System Manager"
            },
            {
                "state": "Pending Finance Review",
                "action": "Reject",
                "next_state": "Rejected",
                "allowed": "Finance Manager"
            },
            {
                "state": "Pending Finance Review",
                "action": "Reject",
                "next_state": "Rejected",
                "allowed": "System Manager"
            },
            {
                "state": "Rejected",
                "action": "Submit for Finance Review",
                "next_state": "Pending Finance Review",
                "allowed": "Accounts User"
            }
        ]
    })
    pi_wf.insert(ignore_permissions=True)
    print(f"Created Workflow: {pi_workflow_name}")

    # 4. Task 8.3: Custom Field on POS Closing Entry for Stock Reconciliation
    custom_field_name = "POS Closing Entry-custom_stock_reconciliation"
    if not frappe.db.exists("Custom Field", custom_field_name):
        cf = frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "POS Closing Entry",
            "fieldname": "custom_stock_reconciliation",
            "label": "Stock Reconciliation",
            "fieldtype": "Link",
            "options": "Stock Reconciliation",
            "insert_after": "pos_profile",
            "description": "Linked Stock Reconciliation document required for branch shift closing."
        })
        cf.insert(ignore_permissions=True)
        print("Created Custom Field: custom_stock_reconciliation on POS Closing Entry")

    # 5. Task 8.3: Server Script for Stock Recon Validation on POS Closing
    ss_name = "Validate Stock Recon on POS Closing"
    if frappe.db.exists("Server Script", ss_name):
        frappe.delete_doc("Server Script", ss_name, force=True)

    ss = frappe.get_doc({
        "doctype": "Server Script",
        "name": ss_name,
        "script_type": "DocType Event",
        "reference_doctype": "POS Closing Entry",
        "doctype_event": "Before Submit",
        "disabled": 0,
        "script": """
if not doc.custom_stock_reconciliation:
    frappe.throw("A valid Stock Reconciliation document is required to close the POS shift.")
else:
    status = frappe.db.get_value("Stock Reconciliation", doc.custom_stock_reconciliation, "docstatus")
    if status != 1:
        frappe.throw("The linked Stock Reconciliation (" + str(doc.custom_stock_reconciliation) + ") must be submitted (docstatus=1) before closing the POS shift.")
"""
    })
    ss.insert(ignore_permissions=True)
    print(f"Created Server Script: {ss_name}")

    # 6. Task 8.3: POS Closing Branch Approval Workflow
    pos_wf_name = "POS Closing Branch Approval"
    if frappe.db.exists("Workflow", pos_wf_name):
        frappe.delete_doc("Workflow", pos_wf_name, force=True)

    pos_wf = frappe.get_doc({
        "doctype": "Workflow",
        "workflow_name": pos_wf_name,
        "document_type": "POS Closing Entry",
        "is_active": 1,
        "override_status": 0,
        "workflow_state_field": "workflow_state",
        "states": [
            {
                "state": "Draft",
                "doc_status": "0",
                "allow_edit": "Accounts User"
            },
            {
                "state": "Pending Branch Manager Approval",
                "doc_status": "0",
                "allow_edit": "Branch Manager"
            },
            {
                "state": "Approved",
                "doc_status": "1",
                "allow_edit": "System Manager"
            }
        ],
        "transitions": [
            {
                "state": "Draft",
                "action": "Submit for Branch Approval",
                "next_state": "Pending Branch Manager Approval",
                "allowed": "Accounts User"
            },
            {
                "state": "Draft",
                "action": "Submit for Branch Approval",
                "next_state": "Pending Branch Manager Approval",
                "allowed": "System Manager"
            },
            {
                "state": "Pending Branch Manager Approval",
                "action": "Approve POS Closing",
                "next_state": "Approved",
                "allowed": "Branch Manager"
            },
            {
                "state": "Pending Branch Manager Approval",
                "action": "Approve POS Closing",
                "next_state": "Approved",
                "allowed": "System Manager"
            }
        ]
    })
    pos_wf.insert(ignore_permissions=True)
    print(f"Created Workflow: {pos_wf_name}")

    frappe.db.commit()
    print("--- Phase 8 Setup Completed Successfully ---")

if __name__ == "__main__":
    run()
