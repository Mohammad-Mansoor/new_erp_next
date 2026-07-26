import frappe
from frappe import _

def execute(filters=None):
	if not filters:
		filters = {}
	elif isinstance(filters, str):
		filters = frappe.parse_json(filters)

	columns = get_columns()
	data = get_data(filters)

	return columns, data

def get_columns():
	return [
		{"fieldname": "item_code", "label": _("Item Code"), "fieldtype": "Link", "options": "Item", "width": 170},
		{"fieldname": "item_name", "label": _("Item Name"), "fieldtype": "Data", "width": 200},
		{"fieldname": "item_group", "label": _("Item Group"), "fieldtype": "Link", "options": "Item Group", "width": 130},
		{"fieldname": "stock_uom", "label": _("Stock UOM"), "fieldtype": "Link", "options": "UOM", "width": 110},
		{"fieldname": "total_qty_sold", "label": _("Total Qty Sold"), "fieldtype": "Float", "width": 130},
		{"fieldname": "total_sales_amount", "label": _("Total Sales Amount (AFN)"), "fieldtype": "Currency", "width": 160},
		{"fieldname": "current_stock_qty", "label": _("Stock On Hand"), "fieldtype": "Float", "width": 130},
		{"fieldname": "reserved_stock_qty", "label": _("Reserved Qty"), "fieldtype": "Float", "width": 120},
		{"fieldname": "available_stock_qty", "label": _("Available Qty"), "fieldtype": "Float", "width": 130},
		{"fieldname": "last_sale_date", "label": _("Last Sale Date"), "fieldtype": "Date", "width": 130}
	]

def get_data(filters):
	company = filters.get("company", "Jahan Kodak")
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	selected_wh = filters.get("warehouse")
	filter_by = (filters.get("filter_by") or "Top Selling").strip()

	wh_sales_clause = ""
	wh_pos_clause = ""
	params = [company, from_date, to_date, company, from_date, to_date]

	if selected_wh:
		wh_sales_clause = " and sii.warehouse = %s "
		wh_pos_clause = " and pii.warehouse = %s "
		params = [company, from_date, to_date, selected_wh, company, from_date, to_date, selected_wh]

	sales_query = f"""
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
			{wh_sales_clause}

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
			{wh_pos_clause}
		) combined_sales
		group by item_code
	"""

	sales_rows = frappe.db.sql(sales_query, tuple(params), as_dict=True)
	items = frappe.get_all("Item", filters={"disabled": 0}, fields=["name", "item_name", "item_group", "stock_uom"])
	sales_map = {row.item_code: row for row in sales_rows}

	data = []
	for item in items:
		item_code = item.name
		item_name = item.item_name
		item_group = item.item_group
		stock_uom = item.stock_uom or ""

		s_info = sales_map.get(item_code)
		total_qty = float(s_info.total_qty) if s_info and s_info.total_qty else 0.0
		total_amount = float(s_info.total_amount) if s_info and s_info.total_amount else 0.0
		last_sale = s_info.last_sale if s_info else None

		bin_data = frappe.db.sql("""
			select 
				sum(actual_qty) as actual_qty,
				sum(reserved_qty) as reserved_qty,
				sum(projected_qty) as projected_qty
			from `tabBin`
			where item_code = %s
			""" + (" and warehouse = %s" if selected_wh else ""), 
			(item_code, selected_wh) if selected_wh else (item_code,), as_dict=True)

		actual_qty = float(bin_data[0].actual_qty) if bin_data and bin_data[0].actual_qty else 0.0
		reserved_qty = float(bin_data[0].reserved_qty) if bin_data and bin_data[0].reserved_qty else 0.0
		available_qty = actual_qty - reserved_qty

		row = {
			"item_code": item_code,
			"item_name": item_name,
			"item_group": item_group,
			"total_qty_sold": total_qty,
			"total_sales_amount": total_amount,
			"stock_uom": stock_uom,
			"current_stock_qty": actual_qty,
			"reserved_stock_qty": reserved_qty,
			"available_stock_qty": available_qty,
			"last_sale_date": last_sale
		}
		data.append(row)

	if filter_by == "Slow Moving":
		# Slow Moving: Lowest sales first (0 sales first), then highest stock sitting on shelves
		data = sorted(data, key=lambda x: (x["total_qty_sold"], -x["current_stock_qty"], -x["available_stock_qty"]))
	else:
		# Top Selling (default): Highest sales first, then highest revenue, then highest stock
		data = sorted(data, key=lambda x: (x["total_qty_sold"], x["total_sales_amount"], x["current_stock_qty"]), reverse=True)

	return data
