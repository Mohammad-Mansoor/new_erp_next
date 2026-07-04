import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def run():
    frappe.flags.in_test = True
    
    # 1. Create Roles
    roles = ["Branch Manager", "Branch User"]
    for role in roles:
        if not frappe.db.exists("Role", role):
            frappe.get_doc({
                "doctype": "Role",
                "role_name": role,
                "desk_access": 1
            }).insert(ignore_permissions=True)
            print(f"Created Role: {role}")

    # 2. Add 'branch' field to Material Request & Purchase Order if missing
    doctypes = ["Material Request", "Purchase Order"]
    for dt in doctypes:
        if not frappe.db.exists("Custom Field", {"dt": dt, "fieldname": "branch"}):
            create_custom_field(dt, {
                "fieldname": "branch",
                "label": "Branch",
                "fieldtype": "Link",
                "options": "Branch",
                "insert_after": "company",
                "reqd": 1
            })
            print(f"Added Branch field to {dt}")

    # 3. Set Apply User Permissions on DocPerms for these roles
    # For Material Request
    if not frappe.db.exists("Custom DocPerm", {"parent": "Material Request", "role": "Branch Manager"}):
        frappe.get_doc({
            "doctype": "Custom DocPerm",
            "parent": "Material Request",
            "role": "Branch Manager",
            "read": 1, "write": 1, "create": 1, "submit": 1,
            "apply_user_permissions": 1
        }).insert(ignore_permissions=True)
        
    if not frappe.db.exists("Custom DocPerm", {"parent": "Material Request", "role": "Branch User"}):
        frappe.get_doc({
            "doctype": "Custom DocPerm",
            "parent": "Material Request",
            "role": "Branch User",
            "read": 1, "write": 1, "create": 1,
            "apply_user_permissions": 1
        }).insert(ignore_permissions=True)

    # 4. Update the Workflow to use Branch Manager role and enable System Notifications (Workflow Actions)
    wf_name = "JK Material Request Flow"
    if frappe.db.exists("Workflow", wf_name):
        wf = frappe.get_doc("Workflow", wf_name)
        # Disable Email Alerts
        wf.send_email_alert = 0 
        
        # In Frappe, Workflow Actions are generated if we create a Workflow Action Master and assign it.
        # Ensure we use Branch Manager for the BM Approve step
        for transition in wf.transitions:
            if transition.action == "BM Approve":
                transition.allowed = "Branch Manager"
                
        wf.save(ignore_permissions=True)
        print("Updated Workflow permissions and disabled emails.")

    frappe.db.commit()
    print("Permissions and Branch isolation setup completed.")
