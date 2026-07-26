import frappe

def run():
    frappe.init(site="development.localhost")
    frappe.connect()

    company = "Jahan Kodak"
    print("--- Starting Phase 9: Human Resources Setup ---")

    # 1. Ensure Roles
    roles = ["HR User", "HR Manager", "Finance Manager"]
    for role_name in roles:
        if not frappe.db.exists("Role", role_name):
            doc = frappe.get_doc({
                "doctype": "Role",
                "role_name": role_name,
                "desk_access": 1
            })
            doc.insert(ignore_permissions=True)
            print(f"Created Role: {role_name}")

    # 2. Configure Leave Types
    leave_types = [
        {"leave_type_name": "Annual Leave", "is_allocable": 1, "max_continuous_days_allowed": 30},
        {"leave_type_name": "Sick Leave", "is_allocable": 1, "max_continuous_days_allowed": 14},
        {"leave_type_name": "Casual Leave", "is_allocable": 1, "max_continuous_days_allowed": 7},
        {"leave_type_name": "Unpaid Leave", "is_allocable": 0, "is_lwp": 1}
    ]
    for lt in leave_types:
        if not frappe.db.exists("Leave Type", lt["leave_type_name"]):
            doc = frappe.get_doc({
                "doctype": "Leave Type",
                **lt
            })
            doc.insert(ignore_permissions=True)
            print(f"Created Leave Type: {lt['leave_type_name']}")

    # 3. Configure Shift Type
    shift_name = "Day Shift"
    if not frappe.db.exists("Shift Type", shift_name):
        doc = frappe.get_doc({
            "doctype": "Shift Type",
            "name": shift_name,
            "shift_name": shift_name,
            "start_time": "08:00:00",
            "end_time": "17:00:00",
            "enable_auto_attendance": 0
        })
        doc.insert(ignore_permissions=True)
        print(f"Created Shift Type: {shift_name}")

    # 4. Configure Salary Components
    earnings = [
        {"salary_component": "Basic Salary", "type": "Earning"},
        {"salary_component": "House Rent Allowance", "type": "Earning"},
        {"salary_component": "Transport Allowance", "type": "Earning"}
    ]
    deductions = [
        {"salary_component": "Income Tax", "type": "Deduction"},
        {"salary_component": "Unpaid Leave Deduction", "type": "Deduction"}
    ]
    for comp in earnings + deductions:
        if not frappe.db.exists("Salary Component", comp["salary_component"]):
            doc = frappe.get_doc({
                "doctype": "Salary Component",
                "salary_component": comp["salary_component"],
                "type": comp["type"],
                "description": f"{comp['type']} component for payroll calculation"
            })
            doc.insert(ignore_permissions=True)
            print(f"Created Salary Component: {comp['salary_component']} ({comp['type']})")

    # 5. Ensure Workflow States & Actions
    states = [
        "Draft", "Pending HR Approval", "Pending Finance Approval",
        "Approved", "Rejected"
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
        "Submit for HR Approval", "Approve HR Review", "Approve Payroll", "Reject Payroll"
    ]
    for act in actions:
        if not frappe.db.exists("Workflow Action Master", act):
            doc = frappe.get_doc({
                "doctype": "Workflow Action Master",
                "workflow_action_name": act
            })
            doc.insert(ignore_permissions=True)
            print(f"Created Workflow Action Master: {act}")

    # 6. Task 9.2: Payroll Entry Approval Workflow
    wf_name = "Payroll Entry Approval"
    if frappe.db.exists("Workflow", wf_name):
        frappe.delete_doc("Workflow", wf_name, force=True)
        print(f"Removed existing Workflow: {wf_name}")

    payroll_wf = frappe.get_doc({
        "doctype": "Workflow",
        "workflow_name": wf_name,
        "document_type": "Payroll Entry",
        "is_active": 1,
        "override_status": 0,
        "workflow_state_field": "workflow_state",
        "states": [
            {
                "state": "Draft",
                "doc_status": "0",
                "allow_edit": "HR User"
            },
            {
                "state": "Pending HR Approval",
                "doc_status": "0",
                "allow_edit": "HR Manager"
            },
            {
                "state": "Pending Finance Approval",
                "doc_status": "0",
                "allow_edit": "Finance Manager"
            },
            {
                "state": "Approved",
                "doc_status": "1",
                "allow_edit": "System Manager"
            },
            {
                "state": "Rejected",
                "doc_status": "0",
                "allow_edit": "HR User"
            }
        ],
        "transitions": [
            {
                "state": "Draft",
                "action": "Submit for HR Approval",
                "next_state": "Pending HR Approval",
                "allowed": "HR User"
            },
            {
                "state": "Draft",
                "action": "Submit for HR Approval",
                "next_state": "Pending HR Approval",
                "allowed": "System Manager"
            },
            {
                "state": "Pending HR Approval",
                "action": "Approve HR Review",
                "next_state": "Pending Finance Approval",
                "allowed": "HR Manager"
            },
            {
                "state": "Pending HR Approval",
                "action": "Approve HR Review",
                "next_state": "Pending Finance Approval",
                "allowed": "System Manager"
            },
            {
                "state": "Pending HR Approval",
                "action": "Reject Payroll",
                "next_state": "Rejected",
                "allowed": "HR Manager"
            },
            {
                "state": "Pending Finance Approval",
                "action": "Approve Payroll",
                "next_state": "Approved",
                "allowed": "Finance Manager"
            },
            {
                "state": "Pending Finance Approval",
                "action": "Approve Payroll",
                "next_state": "Approved",
                "allowed": "System Manager"
            },
            {
                "state": "Pending Finance Approval",
                "action": "Reject Payroll",
                "next_state": "Rejected",
                "allowed": "Finance Manager"
            }
        ]
    })
    payroll_wf.insert(ignore_permissions=True)
    print(f"Created Workflow: {wf_name}")

    frappe.db.commit()
    print("--- Phase 9 Setup Completed Successfully ---")

if __name__ == "__main__":
    run()
