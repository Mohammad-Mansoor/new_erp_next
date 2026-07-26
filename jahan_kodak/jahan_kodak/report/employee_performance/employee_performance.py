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
		{"fieldname": "employee", "label": _("Employee"), "fieldtype": "Link", "options": "Employee", "width": 140},
		{"fieldname": "employee_name", "label": _("Employee Name"), "fieldtype": "Data", "width": 180},
		{"fieldname": "branch", "label": _("Branch"), "fieldtype": "Link", "options": "Branch", "width": 140},
		{"fieldname": "total_invoices", "label": _("Total Sales Invoices"), "fieldtype": "Int", "width": 150},
		{"fieldname": "total_sales_amount", "label": _("Total Sales (AFN)"), "fieldtype": "Currency", "width": 150},
		{"fieldname": "avg_invoice_value", "label": _("Avg Order Value (AFN)"), "fieldtype": "Currency", "width": 160},
		{"fieldname": "attendance_days", "label": _("Days Present"), "fieldtype": "Int", "width": 120}
	]

def get_data(filters):
	company = filters.get("company", "Jahan Kodak")
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	branch = filters.get("branch")

	emp_filters = {"company": company, "status": "Active"}
	if branch:
		emp_filters["branch"] = branch

	employees = frappe.get_all("Employee", filters=emp_filters, fields=["name", "employee_name", "user_id", "branch"])
	if not employees:
		return []

	data = []
	for emp in employees:
		emp_id = emp.name
		emp_name = emp.employee_name
		emp_user = emp.user_id
		emp_branch = emp.branch or ""

		if emp_user:
			sales_data = frappe.db.sql("""
				select count(name), sum(grand_total)
				from `tabSales Invoice`
				where company = %s and owner = %s
				and posting_date between %s and %s
				and docstatus = 1
			""", (company, emp_user, from_date, to_date))
			total_invoices = sales_data[0][0] or 0
			total_sales = sales_data[0][1] or 0.0
		else:
			total_invoices = 0
			total_sales = 0.0

		att_count = frappe.db.sql("""
			select count(name)
			from `tabAttendance`
			where employee = %s
			and attendance_date between %s and %s
			and status = 'Present'
			and docstatus = 1
		""", (emp_id, from_date, to_date))[0][0] or 0

		avg_invoice = (total_sales / total_invoices) if total_invoices > 0 else 0.0

		data.append({
			"employee": emp_id,
			"employee_name": emp_name,
			"branch": emp_branch,
			"total_invoices": total_invoices,
			"total_sales_amount": total_sales,
			"avg_invoice_value": avg_invoice,
			"attendance_days": att_count
		})

	return data
