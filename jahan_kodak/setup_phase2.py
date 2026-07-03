import frappe

def run():
    frappe.flags.in_test = True
    
    # 1. Create Company
    if not frappe.db.exists("Company", "Jahan Kodak"):
        doc = frappe.get_doc({
            "doctype": "Company",
            "company_name": "Jahan Kodak",
            "default_currency": "AFN",
            "country": "Afghanistan",
            "abbr": "JK"
        })
        doc.insert(ignore_permissions=True)
        print("Created Company: Jahan Kodak")
    else:
        print("Company already exists")

    # The root cost center is automatically created as "Jahan Kodak - JK"
    root_cc = "Jahan Kodak - JK"

    # 2. Create Branches and their Cost Centers
    branches = ["Kabul Center", "Shahr-e-Naw", "Karteh Naw", "Macroyan", "Dasht-e-Barchi"]
    for b in branches:
        if not frappe.db.exists("Branch", b):
            doc = frappe.get_doc({
                "doctype": "Branch",
                "branch": b
            })
            doc.insert(ignore_permissions=True)
            print(f"Created Branch: {b}")
        else:
            print(f"Branch '{b}' already exists")

        # Cost Center Name format in ERPNext: "BranchName - Abbr"
        cc_name = f"{b} - JK"
        if not frappe.db.exists("Cost Center", cc_name):
            try:
                cc = frappe.get_doc({
                    "doctype": "Cost Center",
                    "cost_center_name": b,
                    "company": "Jahan Kodak",
                    "parent_cost_center": root_cc,
                    "is_group": 0
                })
                cc.insert(ignore_permissions=True)
                print(f"Created Cost Center: {cc_name}")
            except Exception as e:
                print(f"Failed to create Cost Center {cc_name}: {e}")
        else:
            print(f"Cost Center '{cc_name}' already exists")

    frappe.db.commit()
    print("\nPhase 2 execution successful!")
