import frappe

def run():
    frappe.init(site="development.localhost")
    frappe.connect()

    frappe.flags.in_import = True
    frappe.conf.developer_mode = 1

    print("--- Starting Phase 10: Reports & Dashboards Setup ---")

    reports = [
        {
            "report_name": "Branch Profitability",
            "ref_doctype": "GL Entry",
            "report_type": "Script Report",
            "is_standard": "Yes",
            "module": "Jahan Kodak"
        },
        {
            "report_name": "Employee Performance",
            "ref_doctype": "Sales Invoice",
            "report_type": "Script Report",
            "is_standard": "Yes",
            "module": "Jahan Kodak"
        },
        {
            "report_name": "Top Selling and Slow Moving Items",
            "ref_doctype": "Item",
            "report_type": "Script Report",
            "is_standard": "Yes",
            "module": "Jahan Kodak"
        }
    ]

    roles = ["System Manager", "Branch Manager", "Accounts User"]

    for r in reports:
        report_name = r["report_name"]
        if frappe.db.exists("Report", report_name):
            doc = frappe.get_doc("Report", report_name)
            doc.update(r)
            doc.save(ignore_permissions=True)
            print(f"Updated Report: {report_name}")
        else:
            doc = frappe.get_doc({
                "doctype": "Report",
                **r
            })
            doc.insert(ignore_permissions=True)
            print(f"Created Report: {report_name}")

        # Ensure Role Permissions on Report
        for role_name in roles:
            if frappe.db.exists("Role", role_name):
                has_perm = frappe.db.exists("Has Role", {"parent": report_name, "role": role_name})
                if not has_perm:
                    doc.append("roles", {"role": role_name})
                    doc.save(ignore_permissions=True)

    frappe.db.commit()
    print("--- Phase 10 Setup Completed Successfully ---")

if __name__ == "__main__":
    run()
