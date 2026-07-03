import json

md = []
def P(text=""):
    md.append(text)
def H(level, text):
    md.append(f"{'#' * level} {text}")
def T(task):
    H(4, f"Task {task['id']}: {task['title']}")
    P(f"**Status:** ⬜ Not Started")
    P(f"**Purpose:** {task['purpose']}")
    P(f"**Business Requirement Reference:** {task['req_ref']}")
    P(f"**Workflow Reference:** {task['flow_ref']}")
    P(f"**Description:** {task['desc']}")
    P()
    H(5, "Technical Design")
    P(f"- **ERPNext Module:** {task['tech'].get('module', 'Core')}")
    P(f"- **Doctype Changes:** {task['tech'].get('doctype', 'None')}")
    P(f"- **Custom Fields:** {task['tech'].get('fields', 'None')}")
    P(f"- **Child Tables:** {task['tech'].get('child_tables', 'None')}")
    P(f"- **Server Scripts:** {task['tech'].get('server', 'None')}")
    P(f"- **Client Scripts:** {task['tech'].get('client', 'None')}")
    P(f"- **Python Files:** {task['tech'].get('py', 'None')}")
    P(f"- **JS Files:** {task['tech'].get('js', 'None')}")
    P(f"- **Print Formats:** {task['tech'].get('print', 'None')}")
    P(f"- **Reports:** {task['tech'].get('reports', 'None')}")
    P(f"- **Permissions:** {task['tech'].get('perms', 'System Manager')}")
    P(f"- **Role Changes:** {task['tech'].get('roles', 'None')}")
    P(f"- **Workflow Changes:** {task['tech'].get('workflows', 'None')}")
    P(f"- **Notification Changes:** {task['tech'].get('notifications', 'None')}")
    P()
    H(5, "Impact Analysis")
    P(f"- **Accounting Impact:** {task['impact'].get('acc', 'None')}")
    P(f"- **Stock Impact:** {task['impact'].get('stock', 'None')}")
    P(f"- **HR Impact:** {task['impact'].get('hr', 'None')}")
    P(f"- **API Impact:** {task['impact'].get('api', 'None')}")
    P()
    H(5, "Project Management")
    P(f"- **Dependencies:** {task['pm'].get('deps', 'None')}")
    P(f"- **Estimated Complexity:** {task['pm'].get('complexity', 'Low')}")
    P(f"- **Estimated Time:** {task['pm'].get('time', '1 Hour')}")
    P()
    H(5, "Testing & Quality Assurance")
    P("**Acceptance Criteria:**")
    for a in task['qa'].get('acceptance', []): P(f"- {a}")
    P("\n**Manual Test Cases:**")
    for m in task['qa'].get('manual', []): P(f"- {m}")
    P("\n**Edge Cases:**")
    for e in task['qa'].get('edge', []): P(f"- {e}")
    P("\n**Regression Test Requirements:**")
    for r in task['qa'].get('regression', []): P(f"- {r}")
    P()
    H(5, "Subtasks")
    for s in task['subtasks']: P(f"- [ ] {s}")
    P()
    H(5, "GitHub Workflow & Deployment")
    branch = task.get('git', {}).get('branch', f"feat/TASK-{task['id']}")
    commit = task.get('git', {}).get('commit', f"feat: implement {task['title']}")
    P(f"- **Git Branch Name:** `{branch}`")
    P(f"- **Suggested Commit Message:** `{commit}`")
    P(f"- **Production Deployment Notes:** {task.get('deploy', {}).get('notes', 'Standard migration.')}")
    P(f"- **Rollback Strategy:** {task.get('deploy', {}).get('rollback', 'Git revert and restore database if necessary.')}")
    P("---\n")

def Feature(title, bp, current, req_cust, reason, risk, test, deploy):
    H(3, f"Feature: {title}")
    P(f"**Business Process:** {bp}")
    P(f"**Current ERPNext Behavior:** {current}")
    P(f"**Required Customization:** {req_cust}")
    P(f"**Reason:** {reason}")
    P(f"**Possible Risks:** {risk}")
    P(f"**Testing Strategy:** {test}")
    P(f"**Deployment Strategy:** {deploy}")
    P()

def Header():
    P("# ERPNext Implementation Master Roadmap: Jahan Kodak")
    P("This document serves as the single source of truth for the entire ERPNext customization project. Every developer must strictly follow this plan.")
    P()
    H(2, "Document Conflicts & Resolutions")
    P("During the analysis of the Scope Document (Doc 1) and Workflow Document (Doc 2), the following conflicts were identified and resolved:")
    P("1. **Purchasing Workflow:** Doc 1 states: `Material Request -> Purchase Order`. Doc 2 states: `Material Request -> Request for Quotation (combined) -> Purchase Order -> Cargo/Transit`. **Resolution:** We will combine Material Request and RFQ functionality into a streamlined Material Request process, followed by PO, and implement a custom `In Transit` mechanism (via Transit Warehouses) before `Purchase Receipt`.")
    P("2. **Inventory Valuation:** Doc 1 doesn't specify valuation, but Doc 2 explicitly mandates `Moving Average` for Wholesale. **Resolution:** Moving Average will be enforced at the Company level.")
    P()

Header()

# PHASE 1
H(1, "Phase 1: Project Setup")
H(2, "Module: Development Environment")
Feature("System Initialization", "Initialize the development ecosystem.", "Standard unconfigured bench", "Custom App creation", "Isolate customizations", "Environment misconfigurations", "Developer environment testing", "Automated setup script")
T({
    "id": "1.1", "title": "Create Custom App and Repository",
    "purpose": "Isolate all project customizations in a dedicated Frappe app.",
    "req_ref": "Doc 1 (Scope): ERP Configuration Document", "flow_ref": "Doc 2: Phase 1 As-Is / To-Be",
    "desc": "Initialize `jahan_kodak` custom app and link it to GitHub.",
    "tech": {"module": "Core", "doctype": "None", "py": "hooks.py updates"},
    "impact": {}, "pm": {"deps": "None", "complexity": "Low", "time": "2 Hours"},
    "qa": {"acceptance": ["App created successfully", "Installed on site", "Pushed to GitHub"], "manual": ["bench new-app jahan_kodak", "bench --site site1.local install-app jahan_kodak"], "edge": [], "regression": []},
    "subtasks": ["Create app", "Configure hooks.py", "Initialize Git repo", "Push to GitHub branch 'develop'"]
})

# PHASE 2
H(1, "Phase 2: System Architecture & Master Data")
H(2, "Module: Company & Branches")
Feature("Multi-Branch Architecture", "Company owns multiple branches with independent POS, Cash, and Warehouses.", "Branches are just standard Cost Centers/Warehouses", "Enforce branch-level isolation for cost centers, warehouses, and POS", "Requirement for independent branch profitability", "Data leakage between branches", "Role-based testing per branch", "Export fixtures for standard records")
T({
    "id": "2.1", "title": "Define Company and Base Hierarchy",
    "purpose": "Setup the root company and initial accounting structure.",
    "req_ref": "Doc 1: 1.1", "flow_ref": "Doc 2: Phase 3",
    "desc": "Create Company 'Jahan Kodak', set Valuation to Moving Average. Configure Base Currency.",
    "tech": {"module": "Setup", "doctype": "Company"},
    "impact": {"acc": "Sets base currency and defaults"}, "pm": {"deps": "1.1", "complexity": "Low", "time": "1 Hour"},
    "qa": {"acceptance": ["Company created", "Moving Average set"], "manual": ["Check company doctype"], "edge": [], "regression": []},
    "subtasks": ["Create Company", "Set Valuation Method", "Set default accounts"]
})
T({
    "id": "2.2", "title": "Create Branches (Kabul & Herat/Mazar)",
    "purpose": "Create branch records for each store.",
    "req_ref": "Doc 1: 1.2", "flow_ref": "Doc 2: Phase 3",
    "desc": "Create standard Branches: Kabul Center, Shahr-e-Naw, Karteh Naw, Macroyan, Dasht-e-Barchi, Mazar, Herat.",
    "tech": {"module": "Setup", "doctype": "Branch"},
    "impact": {"acc": "Used for dimension filtering"}, "pm": {"deps": "2.1", "complexity": "Low", "time": "2 Hours"},
    "qa": {"acceptance": ["All branches exist"], "manual": ["List view shows all branches"], "edge": [], "regression": []},
    "subtasks": ["Create Kabul Branches", "Create Mazar Branches", "Create Herat Branches"]
})

H(2, "Module: Item Master & SKU")
Feature("Dynamic SKU & Attributes", "Items need attributes (Size, Color, Brand) and auto-generated SKUs.", "SKUs are manual or basic.", "Auto generate SKU based on Group-Year-Color-Size (e.g. TSH-2026-BLK-L).", "Standardization of 1000s of items.", "SKU collision", "Test item creation", "Fixture export for Item Templates")
T({
    "id": "2.3", "title": "Define Item Attributes (Color, Size, Brand, Season)",
    "purpose": "Setup all variants for clothing.",
    "req_ref": "Doc 1: 2.3", "flow_ref": "Doc 2: Phase 4",
    "desc": "Create Item Attributes: Size (XS, S, M, L, XL), Color (Black, White, Navy), Brand, Season.",
    "tech": {"module": "Stock", "doctype": "Item Attribute"},
    "impact": {"stock": "Defines variant combinations"}, "pm": {"deps": "2.1", "complexity": "Low", "time": "2 Hours"},
    "qa": {"acceptance": ["Attributes created with abbreviations"], "manual": ["Check Item Attribute list"], "edge": [], "regression": []},
    "subtasks": ["Create Size attribute", "Create Color attribute", "Create Brand attribute", "Create Season attribute"]
})
T({
    "id": "2.4", "title": "Automated SKU Generator (Naming Series)",
    "purpose": "Generate SKU automatically as TSH-2026-BLK-L",
    "req_ref": "Doc 1: 2.1", "flow_ref": "Doc 2: Phase 5",
    "desc": "Implement a custom Server Script (Document Event - Before Save on Item) to concatenate Item Group abbreviation + Collection Year + Color Abbreviation + Size Abbreviation.",
    "tech": {"module": "Stock", "doctype": "Item", "server": "Before Save Hook", "py": "item.py hook"},
    "impact": {"stock": "Item ID is auto-set"}, "pm": {"deps": "2.3", "complexity": "Medium", "time": "4 Hours"},
    "qa": {"acceptance": ["SKU matches format TSH-2026-BLK-L"], "manual": ["Create item variant and check ID"], "edge": ["Missing attribute abbreviations"], "regression": []},
    "subtasks": ["Add Abbreviation field to Item Group", "Add Abbreviation field to Attribute Values", "Write Python hook for `autoname`", "Test with variants"]
})
T({
    "id": "2.5", "title": "Barcode and QR Code Generation",
    "purpose": "Auto-generate barcodes and QR codes for Items.",
    "req_ref": "Doc 1: 2.2", "flow_ref": "Doc 2: Phase 4",
    "desc": "Ensure standard ERPNext Barcode generation is enabled. Create a custom Print Format for Item Barcode/QR Code printing.",
    "tech": {"module": "Stock", "doctype": "Item Barcode", "print": "Item Barcode Custom Format"},
    "impact": {}, "pm": {"deps": "2.4", "complexity": "Low", "time": "2 Hours"},
    "qa": {"acceptance": ["Print format prints valid QR/Barcode"], "manual": ["Print from Item screen"], "edge": [], "regression": []},
    "subtasks": ["Enable auto barcode", "Create HTML Print format for labels", "Test scanning"]
})

# PHASE 3
H(1, "Phase 3: Inventory & Warehouses")
H(2, "Module: Warehouse Tree")
Feature("Centralized & Branch Warehouses", "Hierarchy of Central Warehouse -> Branch Warehouses.", "Standard Tree", "Define exact tree structure", "Inventory isolation", "Wrong warehouse selection", "Stock balance tests", "Fixtures")
T({
    "id": "3.1", "title": "Create Warehouse Hierarchy",
    "purpose": "Setup Central and Branch warehouses.",
    "req_ref": "Doc 1: 1.3", "flow_ref": "Doc 2: Phase 7",
    "desc": "Create Central Warehouse (Parent: Men, Women, Kids). Create Branch Warehouses (Parent: Branch).",
    "tech": {"module": "Stock", "doctype": "Warehouse"},
    "impact": {"stock": "Base for all stock ledgers"}, "pm": {"deps": "2.2", "complexity": "Low", "time": "2 Hours"},
    "qa": {"acceptance": ["Tree view matches doc"], "manual": ["View Warehouse Tree"], "edge": [], "regression": []},
    "subtasks": ["Create Central WH", "Create Central child nodes (Men, Women, Kids)", "Create WH for all Branches"]
})
T({
    "id": "3.2", "title": "Branch Transfer Approval Workflow",
    "purpose": "Require manager approval for stock transfers.",
    "req_ref": "Doc 1: 1.5", "flow_ref": "Doc 2: Phase 2",
    "desc": "Create a Workflow on `Stock Entry` (Purpose: Material Transfer). States: Pending Request -> Approved (by Inventory Manager) -> In Transit -> Received.",
    "tech": {"module": "Workflow", "doctype": "Stock Entry", "workflows": "Branch Transfer Workflow"},
    "impact": {"stock": "Controls when stock moves"}, "pm": {"deps": "3.1", "complexity": "Medium", "time": "3 Hours"},
    "qa": {"acceptance": ["Stock entry requires approval"], "manual": ["Branch creates request", "Manager approves", "Branch receives"], "edge": ["Rejection"], "regression": []},
    "subtasks": ["Define Workflow States", "Define Transition Rules", "Assign Roles (Inventory Manager)"]
})

# PHASE 4
H(1, "Phase 4: Purchasing & Transit")
H(2, "Module: Procurement Cycle")
Feature("Custom Purchasing & Transit Flow", "Material Request -> PO -> Transit -> Receipt -> Invoice", "Transit requires custom handling or separate warehouses", "Implement 'In Transit' logic via Transit Warehouses.", "Cargo tracking required by Doc 2", "Lost stock in transit", "End-to-End procurement testing", "Custom Scripts")
T({
    "id": "4.1", "title": "Combine Material Request and RFQ",
    "purpose": "Streamline request process.",
    "req_ref": "Doc 1: 4", "flow_ref": "Doc 2: Phase 9",
    "desc": "Customize Material Request Doctype to include RFQ fields (Supplier Quotes child table). Bypasses standard RFQ doctype to meet Doc 2 requirement.",
    "tech": {"module": "Buying", "doctype": "Material Request", "custom_fields": "Quote Details"},
    "impact": {}, "pm": {"deps": "None", "complexity": "Medium", "time": "4 Hours"},
    "qa": {"acceptance": ["MR acts as RFQ"], "manual": ["Create MR, enter quotes, generate PO"], "edge": [], "regression": []},
    "subtasks": ["Add Supplier Quote Child Table to MR", "Add 'Convert to PO' client script logic"]
})
T({
    "id": "4.2", "title": "Implement Cargo Transit Warehouse Flow",
    "purpose": "Track items in transit.",
    "req_ref": "Doc 2: Phase 9", "flow_ref": "Doc 2: Phase 9",
    "desc": "Create a virtual 'Transit Warehouse'. When PO is shipped by supplier, create Stock Entry (Receive to Transit WH). When received at Central, create Stock Entry (Transit to Central WH). Or use Purchase Receipt to Central WH directly.",
    "tech": {"module": "Stock", "doctype": "Warehouse"},
    "impact": {"stock": "Transit valuation"}, "pm": {"deps": "3.1", "complexity": "Medium", "time": "4 Hours"},
    "qa": {"acceptance": ["Stock shows 'In Transit'"], "manual": ["Execute transit flow"], "edge": [], "regression": []},
    "subtasks": ["Create Transit Warehouse", "Create Custom Button on PO: 'Mark as In Transit'", "Button generates Stock Entry to Transit"]
})
T({
    "id": "4.3", "title": "Landed Cost Voucher & Advance Payments",
    "purpose": "Distribute cargo/customs costs and handle advances.",
    "req_ref": "Doc 2: Phase 9", "flow_ref": "Doc 2: Phase 9",
    "desc": "Train and configure standard Landed Cost Voucher. Configure Payment Entries linked to PO for Advances.",
    "tech": {"module": "Buying", "doctype": "Landed Cost Voucher"},
    "impact": {"acc": "Increases stock valuation"}, "pm": {"deps": "4.2", "complexity": "Low", "time": "2 Hours"},
    "qa": {"acceptance": ["LCV distributes cost correctly"], "manual": ["Create LCV for a PR"], "edge": [], "regression": []},
    "subtasks": ["Setup LCV expense accounts", "Test Advance Payment allocation to Invoice"]
})

# PHASE 5
H(1, "Phase 5: Manufacturing")
H(2, "Module: Internal Production")
Feature("Apparel Manufacturing", "Produce clothing from raw materials (fabric, buttons).", "Standard ERPNext Manufacturing.", "Configure BOMs and Production Orders.", "Internal production required", "Incorrect cost rollups", "BOM testing", "Fixtures")
T({
    "id": "5.1", "title": "Define Raw Materials and BOM",
    "purpose": "Setup BOMs for clothing items.",
    "req_ref": "Doc 1: 5", "flow_ref": "Doc 2: Phase 9",
    "desc": "Define raw materials (Fabric, Thread, Buttons) as Items. Create BOMs for Finished Goods (Shirts).",
    "tech": {"module": "Manufacturing", "doctype": "BOM"},
    "impact": {"stock": "Consumes raw, outputs finished"}, "pm": {"deps": "2.3", "complexity": "Medium", "time": "4 Hours"},
    "qa": {"acceptance": ["BOM correctly calculates cost"], "manual": ["Create BOM, verify costs"], "edge": [], "regression": []},
    "subtasks": ["Create Raw Material Item Groups", "Create sample BOM for a T-Shirt", "Add Operations (Sewing, Cutting) and their costs (Maashat)"]
})
T({
    "id": "5.2", "title": "Production Work Order Flow",
    "purpose": "Execute production.",
    "req_ref": "Doc 1: 5", "flow_ref": "Doc 2: Phase 9",
    "desc": "Implement standard Work Order -> Stock Entry (Material Transfer for Manufacture) -> Stock Entry (Manufacture).",
    "tech": {"module": "Manufacturing", "doctype": "Work Order"},
    "impact": {"stock": "Finished goods added to stock"}, "pm": {"deps": "5.1", "complexity": "Low", "time": "2 Hours"},
    "qa": {"acceptance": ["Work Order completes successfully"], "manual": ["Process full Work Order"], "edge": ["Scrap management"], "regression": []},
    "subtasks": ["Test Work Order creation", "Test Scrap recording", "Validate final item cost"]
})

# PHASE 6
H(1, "Phase 6: POS & Sales")
H(2, "Module: POS Configuration")
Feature("Multi-Register Branch POS", "Each branch has multiple POS registers, cashiers, online/offline support.", "Standard POS", "Configure Profiles per branch and register.", "Retail requirements", "Cash mismatch", "POS testing", "Fixtures")
T({
    "id": "6.1", "title": "POS Profiles and Registers",
    "purpose": "Setup isolated POS for each branch.",
    "req_ref": "Doc 1: 1.4", "flow_ref": "Doc 2: Phase 10",
    "desc": "Create POS Profiles for each branch. Assign Specific Warehouse, Cost Center, and Income Accounts to each. Assign POS Users.",
    "tech": {"module": "Retail", "doctype": "POS Profile"},
    "impact": {"acc": "Routes income and cash accurately"}, "pm": {"deps": "3.1", "complexity": "Medium", "time": "4 Hours"},
    "qa": {"acceptance": ["Users only see their branch POS"], "manual": ["Login as Branch A cashier, open POS"], "edge": ["Offline sync"], "regression": []},
    "subtasks": ["Create POS Profile 'Karteh Parwan 1'", "Create POS Profile 'Karteh Parwan 2'", "Assign Cost Centers", "Assign Warehouses", "Assign Cashiers"]
})
T({
    "id": "6.2", "title": "POS Barcode Scanning & UI Customization",
    "purpose": "Fast checkout for retail.",
    "req_ref": "Doc 1: 6", "flow_ref": "Doc 2: Phase 10",
    "desc": "Ensure Barcode scanning works seamlessly in POS UI. Ensure Fast Search is optimized.",
    "tech": {"module": "Retail", "doctype": "POS Invoice"},
    "impact": {}, "pm": {"deps": "6.1", "complexity": "Low", "time": "2 Hours"},
    "qa": {"acceptance": ["Barcode scan instantly adds item"], "manual": ["Scan barcode in POS"], "edge": [], "regression": []},
    "subtasks": ["Test hardware scanner", "Test Return/Exchange flow in POS"]
})

# PHASE 7
H(1, "Phase 7: Loyalty & Pricing")
H(2, "Module: Loyalty Program")
Feature("Customer Loyalty & Discounts", "2.5% to 5% discount if 6-12 month purchases reach 40k-60k.", "Standard Loyalty Program.", "Configure Loyalty Program points and Pricing Rules.", "Retain customers", "Wrong discount applied", "Checkout testing", "Fixtures")
T({
    "id": "7.1", "title": "Configure Loyalty Program",
    "purpose": "Award points for purchases.",
    "req_ref": "Doc 1: 7", "flow_ref": "Doc 2: Phase 12",
    "desc": "Create Loyalty Program. 1 Point = X Currency. Set point redemption rules.",
    "tech": {"module": "Retail", "doctype": "Loyalty Program"},
    "impact": {"acc": "Expense account for loyalty"}, "pm": {"deps": "6.1", "complexity": "Medium", "time": "3 Hours"},
    "qa": {"acceptance": ["Points awarded and redeemed"], "manual": ["Make POS sale, check customer points"], "edge": ["Returns"], "regression": []},
    "subtasks": ["Setup Loyalty Program", "Setup Loyalty Expense Account"]
})
T({
    "id": "7.2", "title": "Volume/Value Discount Automated Rules",
    "purpose": "Apply 2.5% or 5% discount based on historical spend.",
    "req_ref": "Doc 2: Phase 12", "flow_ref": "Doc 2: Phase 12",
    "desc": "Create a custom Scheduled Job (Nightly) that checks Customer total spend in last 6-12 months. If > 40k, assign Customer Group 'VIP-2.5'. If > 60k, assign 'VIP-5'. Create Pricing Rules for these groups.",
    "tech": {"module": "Accounts", "doctype": "Pricing Rule", "py": "Scheduled Job"},
    "impact": {"acc": "Reduces revenue"}, "pm": {"deps": "7.1", "complexity": "High", "time": "6 Hours"},
    "qa": {"acceptance": ["Customers automatically upgraded and get discount"], "manual": ["Run script manually, check Customer Group", "Make POS sale, check discount"], "edge": ["Downgrading customers"], "regression": []},
    "subtasks": ["Create Customer Groups (VIP-2.5, VIP-5)", "Create Pricing Rules for groups", "Write python script for historical spend calculation", "Setup Scheduled Job"]
})

# PHASE 8
H(1, "Phase 8: Financial Management")
H(2, "Module: Chart of Accounts & Closing")
Feature("Finance setup and Daily Closing", "Branch-level accounting, expenses, and daily reconciliation.", "Standard Accounts", "Setup complete COA, Cash/Bank accounts, and daily closing workflow.", "Core financial reporting", "Reconciliation errors", "Balance testing", "Fixtures")
T({
    "id": "8.1", "title": "Implement Chart of Accounts",
    "purpose": "Map to Afghan retail requirements.",
    "req_ref": "Doc 1: Accounting", "flow_ref": "Doc 2: Phase 13",
    "desc": "Create COA: Cash & Bank, Advances, Inventory, AR, Fixed Assets, AP, ST/LT Debt, Equity, Retained Earnings, Sales, COGS, Branch Expenses, Marketing, Payroll, Food, Electricity.",
    "tech": {"module": "Accounts", "doctype": "Account"},
    "impact": {"acc": "Core structure"}, "pm": {"deps": "2.1", "complexity": "High", "time": "5 Hours"},
    "qa": {"acceptance": ["COA matches Doc 2 list"], "manual": ["Review Tree view"], "edge": [], "regression": []},
    "subtasks": ["Create Asset Accounts", "Create Liability Accounts", "Create Equity Accounts", "Create Income/Expense Accounts"]
})
T({
    "id": "8.2", "title": "Cost Centers and Profit Centers",
    "purpose": "Track Branch P&L.",
    "req_ref": "Doc 1: Accounting", "flow_ref": "Doc 2: Phase 13",
    "desc": "Create Cost Centers for each Branch. Enforce Cost Center selection on all income/expense transactions.",
    "tech": {"module": "Accounts", "doctype": "Cost Center"},
    "impact": {"acc": "Filters P&L by branch"}, "pm": {"deps": "8.1", "complexity": "Low", "time": "2 Hours"},
    "qa": {"acceptance": ["Cost centers exist for all branches"], "manual": ["Check list"], "edge": [], "regression": []},
    "subtasks": ["Create Cost Center Tree", "Set default cost centers on POS Profiles"]
})
T({
    "id": "8.3", "title": "Expense Approval Workflow",
    "purpose": "Managers must approve branch expenses.",
    "req_ref": "Doc 1: Accounting", "flow_ref": "Doc 1: Accounting",
    "desc": "Create Workflow on Journal Entry / Payment Entry for Expenses. Cashier Requests -> Branch Manager Approves -> Central Finance Pays/Validates.",
    "tech": {"module": "Workflow", "doctype": "Journal Entry"},
    "impact": {"acc": "Stops unapproved expenses"}, "pm": {"deps": "8.2", "complexity": "Medium", "time": "3 Hours"},
    "qa": {"acceptance": ["Expenses require approval"], "manual": ["Submit expense"], "edge": [], "regression": []},
    "subtasks": ["Define Workflow", "Test with different roles"]
})
T({
    "id": "8.4", "title": "Daily Cash Closing Procedure",
    "purpose": "Reconcile daily branch POS.",
    "req_ref": "Doc 1: Accounting", "flow_ref": "Doc 2: Phase 14",
    "desc": "Implement POS Closing Voucher process. Cashier submits expected cash vs actual cash. Branch manager validates.",
    "tech": {"module": "Retail", "doctype": "POS Closing Entry"},
    "impact": {"acc": "Consolidates POS invoices to Ledger"}, "pm": {"deps": "6.1", "complexity": "Low", "time": "2 Hours"},
    "qa": {"acceptance": ["Closing entry generates correct GL"], "manual": ["Run POS shift, close shift"], "edge": ["Short/over cash"], "regression": []},
    "subtasks": ["Train users on POS Closing", "Setup Cash difference accounts"]
})

# PHASE 9
H(1, "Phase 9: Human Resources")
H(2, "Module: HRMS")
Feature("Employee Management", "Contracts, Attendance, Payroll.", "Standard HRMS", "Install HRMS app and configure payroll.", "Employee tracking", "Payroll miscalculation", "Payroll testing", "None")
T({
    "id": "9.1", "title": "Install and Configure HRMS",
    "purpose": "Manage Employees.",
    "req_ref": "Doc 1: 8", "flow_ref": "Doc 2: Phase 15",
    "desc": "Install Frappe HR. Setup Employee master, Salary Components, Salary Structures.",
    "tech": {"module": "HR", "doctype": "Employee"},
    "impact": {"hr": "Full employee management", "acc": "Payroll hits expense accounts"}, "pm": {"deps": "1.1", "complexity": "Medium", "time": "4 Hours"},
    "qa": {"acceptance": ["Payroll slip generates correctly"], "manual": ["Process a month payroll"], "edge": [], "regression": []},
    "subtasks": ["Install HRMS", "Create Salary Components (Maash, Kasryat)", "Create Salary Structure", "Link to Payroll expense account"]
})

# PHASE 10
H(1, "Phase 10: Reports & Dashboards")
H(2, "Module: Custom Reporting")
Feature("Managerial Reports", "15+ custom reports for sales, stock, performance.", "Standard reports exist but need tuning.", "Develop Script Reports / Query Reports.", "Management visibility", "Slow queries", "Data testing", "Python/JS files")
T({
    "id": "10.1", "title": "Branch Profitability & Executive Dashboard",
    "purpose": "Show P&L per branch, daily sales, top items.",
    "req_ref": "Doc 1: 9", "flow_ref": "Doc 2: Phase 17",
    "desc": "Create Custom Workspace (Executive Dashboard) with charts: Sales Today, Sales This Month, Gross Profit, Net Profit, Total Stock Value, Branch Stock Value, Debtors, Creditors, Cash. Create Script Report: 'Branch Performance Comparison'.",
    "tech": {"module": "Custom", "doctype": "Workspace", "reports": "Branch Performance"},
    "impact": {}, "pm": {"deps": "8.2", "complexity": "High", "time": "8 Hours"},
    "qa": {"acceptance": ["Dashboard loads correctly", "Numbers match GL"], "manual": ["View dashboard"], "edge": [], "regression": []},
    "subtasks": ["Create Number Cards", "Create Charts", "Create Executive Workspace", "Develop Branch Performance Script Report"]
})
T({
    "id": "10.2", "title": "Stock Movement & Top Selling Reports",
    "purpose": "Analyze inventory.",
    "req_ref": "Doc 1: 9", "flow_ref": "Doc 2: Phase 17",
    "desc": "Create Reports: 'Slow Moving Items', 'Top Selling Items (across all branches)', 'Low Stock Alerts'.",
    "tech": {"module": "Stock", "reports": "Top Selling Items"},
    "impact": {}, "pm": {"deps": "2.4", "complexity": "Medium", "time": "4 Hours"},
    "qa": {"acceptance": ["Reports accurate"], "manual": ["Run report"], "edge": [], "regression": []},
    "subtasks": ["Develop Top Selling Query Report", "Develop Slow Moving Query Report"]
})

# PHASE 11
H(1, "Phase 11: Data Migration")
H(2, "Module: Data Import")
Feature("Initial Data Loading", "Import Items, Customers, Suppliers, Opening Balances.", "Data Import Tool", "Prepare templates and import.", "System Go-Live", "Corrupted data", "Balance validation", "None")
T({
    "id": "11.1", "title": "Import Master Data & Opening Balances",
    "purpose": "Load legacy data.",
    "req_ref": "Doc 1: 10", "flow_ref": "Doc 2: Phase 20",
    "desc": "Import Item Master (with variants), Customers, Suppliers. Import Opening Stock (Stock Entry - Material Receipt). Import Opening Financial Balances (Journal Entry).",
    "tech": {"module": "Data Import", "doctype": "Various"},
    "impact": {"acc": "Opening GL balances", "stock": "Opening Stock ledger"}, "pm": {"deps": "10.2", "complexity": "High", "time": "16 Hours"},
    "qa": {"acceptance": ["Trial balance matches legacy system", "Stock valuation matches legacy system"], "manual": ["Check TB", "Check Stock Balance"], "edge": [], "regression": []},
    "subtasks": ["Import Items", "Import Customers", "Import Suppliers", "Import Stock", "Import Accounts"]
})

# PHASE 12
H(1, "Phase 12: Testing, Training & Deployment")
H(2, "Module: Go-Live")
Feature("UAT & Go-Live", "Test, Train, Deploy.", "N/A", "Execute UAT, User Training, and Phased Rollout.", "Requirement", "System failure", "UAT Scenarios", "Production Deployment")
T({
    "id": "12.1", "title": "User Acceptance Testing (UAT)",
    "purpose": "Validate system with real users.",
    "req_ref": "Doc 1: 12", "flow_ref": "Doc 2: Phase 21",
    "desc": "Execute scenarios: Sales (Normal, Return, Discount), Purchase (Order, Receipt, Pay), Transfer (Central to Branch), Inventory Count.",
    "tech": {"module": "All", "doctype": "All"},
    "impact": {}, "pm": {"deps": "11.1", "complexity": "Medium", "time": "24 Hours"},
    "qa": {"acceptance": ["All UAT signed off"], "manual": ["Run UAT scenarios with client"], "edge": [], "regression": []},
    "subtasks": ["Write UAT Scripts", "Execute Sales UAT", "Execute Purchase UAT", "Execute Transfer UAT", "Fix Bugs"]
})
T({
    "id": "12.2", "title": "User Training",
    "purpose": "Train staff.",
    "req_ref": "Doc 1: 11", "flow_ref": "Doc 2: Phase 22",
    "desc": "Train Cashiers (POS), Inventory Managers, Accountants, Branch Managers.",
    "tech": {"module": "None"},
    "impact": {}, "pm": {"deps": "12.1", "complexity": "Low", "time": "16 Hours"},
    "qa": {"acceptance": ["Staff can use system"], "manual": [], "edge": [], "regression": []},
    "subtasks": ["Cashier Training", "Inventory Training", "Accountant Training", "Manager Training"]
})
T({
    "id": "12.3", "title": "Phased Production Rollout (Go-Live)",
    "purpose": "Deploy system incrementally.",
    "req_ref": "Doc 2: Phase 23", "flow_ref": "Doc 2: Phase 23, 24",
    "desc": "Phase 1 Rollout: Central Warehouse + 1 Branch (2-4 weeks). Phase 2: All Branches. Support for 3 months post Go-Live.",
    "tech": {"module": "Deployment"},
    "impact": {}, "pm": {"deps": "12.2", "complexity": "High", "time": "40 Hours"},
    "qa": {"acceptance": ["System live in production"], "manual": [], "edge": [], "regression": []},
    "subtasks": ["Setup Production Server", "Deploy Custom App", "Go-Live Phase 1", "Go-Live Phase 2", "Commence Support"]
})

with open('/home/anonymous/projects/erp_next/docs/ERPNext_Implementation_Plan.md', 'w') as f:
    f.write('\n'.join(md))

print("Plan generated successfully.")
