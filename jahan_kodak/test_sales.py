import frappe

def run():
    frappe.init(site="development.localhost")
    frappe.connect()

    company = "Jahan Kodak"
    from_date = "2026-07-01"
    to_date = "2026-07-31"

    sales_query = """
        select 
            item_code, 
            max(item_name) as item_name, 
            max(item_group) as item_group, 
            sum(qty) as total_qty, 
            sum(amount) as total_amount, 
            max(posting_date) as last_sale
        from (
            select 
                sii.item_code, 
                sii.item_name, 
                sii.item_group, 
                sii.qty, 
                sii.amount, 
                si.posting_date
            from `tabSales Invoice Item` sii
            join `tabSales Invoice` si on sii.parent = si.name
            where si.company = %s 
            and si.posting_date between %s and %s
            and si.docstatus = 1

            union all

            select 
                pii.item_code, 
                pii.item_name, 
                pii.item_group, 
                pii.qty, 
                pii.amount, 
                pi.posting_date
            from `tabPOS Invoice Item` pii
            join `tabPOS Invoice` pi on pii.parent = pi.name
            where pi.company = %s 
            and pi.posting_date between %s and %s
            and pi.docstatus = 1
        ) combined_sales
        group by item_code
    """

    params = (company, from_date, to_date, company, from_date, to_date)
    rows = frappe.db.sql(sales_query, params, as_dict=True)
    print("SALES ROWS:", rows)

if __name__ == "__main__":
    run()
