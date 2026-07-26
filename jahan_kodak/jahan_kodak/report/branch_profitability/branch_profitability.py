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
		{"fieldname": "cost_center", "label": _("Cost Center / Branch"), "fieldtype": "Link", "options": "Cost Center", "width": 220},
		{"fieldname": "gross_sales", "label": _("Gross Sales (AFN)"), "fieldtype": "Currency", "width": 140},
		{"fieldname": "sales_returns", "label": _("Sales Returns (AFN)"), "fieldtype": "Currency", "width": 140},
		{"fieldname": "net_sales", "label": _("Net Revenue (AFN)"), "fieldtype": "Currency", "width": 140},
		{"fieldname": "cogs", "label": _("COGS (AFN)"), "fieldtype": "Currency", "width": 130},
		{"fieldname": "gross_profit", "label": _("Gross Profit (AFN)"), "fieldtype": "Currency", "width": 140},
		{"fieldname": "operating_expenses", "label": _("Operating Expenses (AFN)"), "fieldtype": "Currency", "width": 160},
		{"fieldname": "loyalty_expense", "label": _("Loyalty Expense (AFN)"), "fieldtype": "Currency", "width": 150},
		{"fieldname": "net_profit", "label": _("Net Profit (AFN)"), "fieldtype": "Currency", "width": 140}
	]

def get_data(filters):
	company = filters.get("company", "Jahan Kodak")
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	selected_cc = filters.get("cost_center")

	cc_filters = {"company": company, "is_group": 0}
	if selected_cc:
		cc_filters["name"] = selected_cc

	cost_centers = frappe.get_all("Cost Center", filters=cc_filters, fields=["name", "cost_center_name"])
	if not cost_centers:
		return []

	data = []
	for cc in cost_centers:
		cc_name = cc.name

		# Get income (Sales)
		income = frappe.db.sql("""
			select sum(credit - debit)
			from `tabGL Entry` gle
			join `tabAccount` acc on gle.account = acc.name
			where gle.company = %s and gle.cost_center = %s
			and gle.posting_date between %s and %s
			and acc.root_type = 'Income'
			and gle.is_cancelled = 0
		""", (company, cc_name, from_date, to_date))[0][0] or 0.0

		# Get COGS
		cogs = frappe.db.sql("""
			select sum(debit - credit)
			from `tabGL Entry` gle
			join `tabAccount` acc on gle.account = acc.name
			where gle.company = %s and gle.cost_center = %s
			and gle.posting_date between %s and %s
			and acc.account_type = 'Cost of Goods Sold'
			and gle.is_cancelled = 0
		""", (company, cc_name, from_date, to_date))[0][0] or 0.0

		# Get Loyalty Expense specifically
		loyalty_exp = frappe.db.sql("""
			select sum(debit - credit)
			from `tabGL Entry` gle
			join `tabAccount` acc on gle.account = acc.name
			where gle.company = %s and gle.cost_center = %s
			and gle.posting_date between %s and %s
			and acc.account_name like '%%Loyalty Program Expense%%'
			and gle.is_cancelled = 0
		""", (company, cc_name, from_date, to_date))[0][0] or 0.0

		# Get all other operating expenses
		other_expenses = frappe.db.sql("""
			select sum(debit - credit)
			from `tabGL Entry` gle
			join `tabAccount` acc on gle.account = acc.name
			where gle.company = %s and gle.cost_center = %s
			and gle.posting_date between %s and %s
			and acc.root_type = 'Expense'
			and acc.account_type != 'Cost of Goods Sold'
			and acc.account_name not like '%%Loyalty Program Expense%%'
			and gle.is_cancelled = 0
		""", (company, cc_name, from_date, to_date))[0][0] or 0.0

		gross_sales = income if income > 0 else 0.0
		sales_returns = abs(income) if income < 0 else 0.0
		net_sales = gross_sales - sales_returns
		gross_profit = net_sales - cogs
		net_profit = gross_profit - (other_expenses + loyalty_exp)

		data.append({
			"cost_center": cc_name,
			"gross_sales": gross_sales,
			"sales_returns": sales_returns,
			"net_sales": net_sales,
			"cogs": cogs,
			"gross_profit": gross_profit,
			"operating_expenses": other_expenses,
			"loyalty_expense": loyalty_exp,
			"net_profit": net_profit
		})

	return data
