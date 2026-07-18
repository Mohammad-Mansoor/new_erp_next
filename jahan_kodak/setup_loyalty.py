import frappe

def run():
    frappe.init(site="development.localhost")
    frappe.connect()
    
    company = "Jahan Kodak"
    
    # 1. Create Expense Account
    expense_account = "Loyalty Program Expense - JK"
    if not frappe.db.exists("Account", expense_account):
        doc = frappe.get_doc({
            "doctype": "Account",
            "account_name": "Loyalty Program Expense",
            "parent_account": "Indirect Expenses - JK",
            "company": company,
            "is_group": 0,
            "account_type": "Expense Account"
        })
        doc.insert(ignore_permissions=True)
        print(f"Created Account: {expense_account}")
        
    # 2. Create Customer Group
    customer_group = "Loyalty Members"
    if not frappe.db.exists("Customer Group", customer_group):
        doc = frappe.get_doc({
            "doctype": "Customer Group",
            "customer_group_name": customer_group,
            "parent_customer_group": "All Customer Groups"
        })
        doc.insert(ignore_permissions=True)
        print(f"Created Customer Group: {customer_group}")
        
    # 3. Create Loyalty Program
    loyalty_program = "Jahan Kodak Rewards"
    if not frappe.db.exists("Loyalty Program", loyalty_program):
        doc = frappe.get_doc({
            "doctype": "Loyalty Program",
            "loyalty_program_name": loyalty_program,
            "from_date": frappe.utils.nowdate(),
            "customer_group": customer_group,
            "auto_opt_in": 1,
            "conversion_factor": 1.0,  # 1 point = 1 unit of currency
            "expense_account": expense_account,
            "company": company,
            "expiry_duration": 365,
            "collection_rules": [
                {
                    "tier_name": "Bronze",
                    "min_spent": 0,
                    "collection_factor": 100.0 # 1 point per 100 spent
                },
                {
                    "tier_name": "Silver",
                    "min_spent": 50000,
                    "collection_factor": 50.0 # 1 point per 50 spent (Better reward)
                },
                {
                    "tier_name": "Gold",
                    "min_spent": 200000,
                    "collection_factor": 25.0 # 1 point per 25 spent (Best reward)
                }
            ]
        })
        doc.insert(ignore_permissions=True)
        print(f"Created Loyalty Program: {loyalty_program}")

    frappe.db.commit()
    print("Setup completed successfully.")

if __name__ == "__main__":
    run()
