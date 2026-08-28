import frappe

def main():
    frappe.init(site="development.localhost")
    frappe.connect()

    custom_fields = [
        {
            "dt": "POS Exchange",
            "fieldname": "payload_hash",
            "label": "Payload Hash",
            "fieldtype": "Data",
            "read_only": 1,
            "insert_after": "idempotency_key"
        }
    ]

    for field in custom_fields:
        if not frappe.db.exists("Custom Field", {"dt": field["dt"], "fieldname": field["fieldname"]}):
            frappe.get_doc({
                "doctype": "Custom Field",
                **field
            }).insert(ignore_permissions=True)

    frappe.db.commit()
    print("Schema updated successfully")

if __name__ == "__main__":
    main()
