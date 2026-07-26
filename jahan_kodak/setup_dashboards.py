import frappe
import json

def run():
	print("--- Setting up Jahan Kodak Executive Dashboards & Statistics ---")
	frappe.flags.in_import = True
	frappe.conf.developer_mode = 1

	create_number_cards()
	create_dashboard_charts()
	create_dashboard()
	create_workspace()

	frappe.db.commit()
	print("--- Dashboards & Statistics Setup Completed Successfully ---")

def create_number_cards():
	cards = [
		{
			"name": "JK Monthly POS Sales",
			"label": "Monthly POS Sales (AFN)",
			"function": "Sum",
			"document_type": "POS Invoice",
			"aggregate_function_based_on": "grand_total",
			"filters_json": json.dumps([
				["POS Invoice", "company", "=", "Jahan Kodak", False],
				["POS Invoice", "docstatus", "=", 1, False]
			]),
			"color": "#2ecc71"
		},
		{
			"name": "JK Total Inventory Value",
			"label": "Total Stock Valuation (AFN)",
			"function": "Sum",
			"document_type": "Bin",
			"aggregate_function_based_on": "stock_value",
			"filters_json": json.dumps([
				["Bin", "stock_value", ">", 0, False]
			]),
			"color": "#3498db"
		},
		{
			"name": "JK Active Employees",
			"label": "Active Staff Count",
			"function": "Count",
			"document_type": "Employee",
			"aggregate_function_based_on": "",
			"filters_json": json.dumps([
				["Employee", "company", "=", "Jahan Kodak", False],
				["Employee", "status", "=", "Active", False]
			]),
			"color": "#9b59b6"
		},
		{
			"name": "JK Pending Material Requests",
			"label": "Pending Stock Transfer Requests",
			"function": "Count",
			"document_type": "Material Request",
			"aggregate_function_based_on": "",
			"filters_json": json.dumps([
				["Material Request", "company", "=", "Jahan Kodak", False],
				["Material Request", "docstatus", "=", 0, False]
			]),
			"color": "#e67e22"
		},
		{
			"name": "JK Outstanding Customer Receivables",
			"label": "Outstanding Receivables (AFN)",
			"function": "Sum",
			"document_type": "Sales Invoice",
			"aggregate_function_based_on": "outstanding_amount",
			"filters_json": json.dumps([
				["Sales Invoice", "company", "=", "Jahan Kodak", False],
				["Sales Invoice", "docstatus", "=", 1, False],
				["Sales Invoice", "outstanding_amount", ">", 0, False]
			]),
			"color": "#e74c3c"
		},
		{
			"name": "JK Loyalty Points Granted",
			"label": "Total Loyalty Points Issued",
			"function": "Sum",
			"document_type": "Loyalty Point Entry",
			"aggregate_function_based_on": "loyalty_points",
			"filters_json": json.dumps([
				["Loyalty Point Entry", "company", "=", "Jahan Kodak", False]
			]),
			"color": "#f1c40f"
		}
	]

	for c in cards:
		if frappe.db.exists("Number Card", c["name"]):
			doc = frappe.get_doc("Number Card", c["name"])
		else:
			doc = frappe.new_doc("Number Card")
			doc.name = c["name"]

		doc.label = c["label"]
		doc.function = c["function"]
		doc.document_type = c["document_type"]
		doc.aggregate_function_based_on = c["aggregate_function_based_on"]
		doc.filters_json = c["filters_json"]
		doc.color = c["color"]
		doc.is_standard = 1
		doc.module = "Jahan Kodak"
		doc.save(ignore_permissions=True)
		print(f"Number Card '{c['name']}' saved.")

def create_dashboard_charts():
	charts = [
		{
			"name": "JK Branch Sales Distribution",
			"chart_name": "Branch POS Sales Distribution",
			"chart_type": "Group By",
			"type": "Bar",
			"document_type": "POS Invoice",
			"group_by_based_on": "cost_center",
			"group_by_type": "Sum",
			"aggregate_function_based_on": "grand_total",
			"based_on": "posting_date",
			"filters_json": json.dumps([
				["POS Invoice", "company", "=", "Jahan Kodak", False],
				["POS Invoice", "docstatus", "=", 1, False]
			]),
			"color": "#2ecc71"
		},
		{
			"name": "JK Daily POS Sales Trend",
			"chart_name": "Daily POS Sales Trend",
			"chart_type": "Sum",
			"type": "Line",
			"document_type": "POS Invoice",
			"based_on": "posting_date",
			"aggregate_function_based_on": "grand_total",
			"timespan": "Last Month",
			"time_interval": "Daily",
			"filters_json": json.dumps([
				["POS Invoice", "company", "=", "Jahan Kodak", False],
				["POS Invoice", "docstatus", "=", 1, False]
			]),
			"color": "#3498db"
		},
		{
			"name": "JK Stock Valuation By Warehouse",
			"chart_name": "Stock Valuation By Warehouse",
			"chart_type": "Group By",
			"type": "Donut",
			"document_type": "Bin",
			"group_by_based_on": "warehouse",
			"group_by_type": "Sum",
			"aggregate_function_based_on": "stock_value",
			"based_on": "creation",
			"filters_json": json.dumps([
				["Bin", "stock_value", ">", 0, False]
			]),
			"color": "#e67e22"
		}
	]

	for ch in charts:
		if frappe.db.exists("Dashboard Chart", ch["name"]):
			doc = frappe.get_doc("Dashboard Chart", ch["name"])
		else:
			doc = frappe.new_doc("Dashboard Chart")
			doc.name = ch["name"]

		doc.chart_name = ch["chart_name"]
		doc.chart_type = ch["chart_type"]
		doc.type = ch["type"]
		doc.document_type = ch["document_type"]
		if "group_by_based_on" in ch:
			doc.group_by_based_on = ch["group_by_based_on"]
		if "group_by_type" in ch:
			doc.group_by_type = ch["group_by_type"]
		if "based_on" in ch:
			doc.based_on = ch["based_on"]
		if "timespan" in ch:
			doc.timespan = ch["timespan"]
		if "time_interval" in ch:
			doc.time_interval = ch["time_interval"]
		doc.aggregate_function_based_on = ch["aggregate_function_based_on"]
		doc.filters_json = ch["filters_json"]
		doc.color = ch["color"]
		doc.is_standard = 1
		doc.module = "Jahan Kodak"
		doc.save(ignore_permissions=True)
		print(f"Dashboard Chart '{ch['name']}' saved.")

def create_dashboard():
	dashboard_name = "Jahan Kodak Executive Dashboard"
	if frappe.db.exists("Dashboard", dashboard_name):
		doc = frappe.get_doc("Dashboard", dashboard_name)
	else:
		doc = frappe.new_doc("Dashboard")
		doc.dashboard_name = dashboard_name

	doc.is_standard = 1
	doc.module = "Jahan Kodak"

	card_links = [
		"JK Monthly POS Sales",
		"JK Total Inventory Value",
		"JK Active Employees",
		"JK Pending Material Requests",
		"JK Outstanding Customer Receivables",
		"JK Loyalty Points Granted"
	]
	doc.cards = []
	for card in card_links:
		doc.append("cards", {"card": card})

	chart_links = [
		"JK Branch Sales Distribution",
		"JK Daily POS Sales Trend",
		"JK Stock Valuation By Warehouse"
	]
	doc.charts = []
	for chart in chart_links:
		doc.append("charts", {"chart": chart, "width": "Half"})

	doc.save(ignore_permissions=True)
	print(f"Dashboard '{dashboard_name}' saved.")

def create_workspace():
	workspace_name = "Jahan Kodak Executive"
	if frappe.db.exists("Workspace", workspace_name):
		doc = frappe.get_doc("Workspace", workspace_name)
	else:
		doc = frappe.new_doc("Workspace")
		doc.name = workspace_name

	doc.label = "Jahan Kodak Executive"
	doc.title = "Jahan Kodak Executive"
	doc.category = "Modules"
	doc.icon = "chart"
	doc.is_standard = 1
	doc.module = "Jahan Kodak"
	doc.public = 1

	# Shortcuts
	shortcuts = [
		{"type": "Report", "link_to": "Branch Profitability", "label": "Branch Profitability Report"},
		{"type": "Report", "link_to": "Employee Performance", "label": "Employee Performance Report"},
		{"type": "Report", "link_to": "Top Selling and Slow Moving Items", "label": "Top Selling & Slow Moving Items Report"},
		{"type": "DocType", "link_to": "POS Invoice", "label": "POS Invoices"},
		{"type": "DocType", "link_to": "Sales Invoice", "label": "Sales Invoices"},
		{"type": "DocType", "link_to": "Employee", "label": "Employees"},
		{"type": "DocType", "link_to": "Stock Entry", "label": "Stock Movements"}
	]
	doc.shortcuts = []
	for sc in shortcuts:
		doc.append("shortcuts", sc)

	# Links
	links = [
		{"type": "Card Break", "label": "Key Custom Reports"},
		{"type": "Link", "link_to": "Branch Profitability", "link_type": "Report", "label": "Branch Profitability"},
		{"type": "Link", "link_to": "Employee Performance", "link_type": "Report", "label": "Employee Performance"},
		{"type": "Link", "link_to": "Top Selling and Slow Moving Items", "link_type": "Report", "label": "Top Selling & Slow Moving Items"},
		{"type": "Card Break", "label": "Core Operations"},
		{"type": "Link", "link_to": "POS Invoice", "link_type": "DocType", "label": "Point of Sale (POS) Invoices"},
		{"type": "Link", "link_to": "Material Request", "link_type": "DocType", "label": "Material / Stock Requests"},
		{"type": "Link", "link_to": "Employee", "link_type": "DocType", "label": "Staff Directory"},
		{"type": "Link", "link_to": "Payroll Entry", "link_type": "DocType", "label": "Monthly Payroll Processing"}
	]
	doc.links = []
	for l in links:
		doc.append("links", l)

	# Charts content
	doc.charts = []
	doc.append("charts", {"chart_name": "JK Branch Sales Distribution", "label": "Branch Sales Distribution"})
	doc.append("charts", {"chart_name": "JK Stock Valuation By Warehouse", "label": "Stock Valuation By Warehouse"})

	# Number cards content
	doc.number_cards = []
	doc.append("number_cards", {"number_card_name": "JK Monthly POS Sales", "label": "Monthly POS Sales"})
	doc.append("number_cards", {"number_card_name": "JK Total Inventory Value", "label": "Total Stock Value"})
	doc.append("number_cards", {"number_card_name": "JK Active Employees", "label": "Active Employees"})
	doc.append("number_cards", {"number_card_name": "JK Pending Material Requests", "label": "Pending Stock Transfers"})

	doc.save(ignore_permissions=True)
	print(f"Workspace '{workspace_name}' saved.")
