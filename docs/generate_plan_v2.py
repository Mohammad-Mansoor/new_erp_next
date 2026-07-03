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
    branch = task.get('git', {}).get('branch', f"feat/TASK-{task['id'].replace('.','-')}")
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
    P("During the analysis of the Scope Document (Doc 1) and JK-Workflow PDF (Doc 2), the following conflicts and refinements were identified:")
    P("1. **Procurement Approvals:** Doc 1 has a basic procurement flow. JK-Workflow requires multi-level approval for Material Request (`Branch Manager -> Procurement Approval`) and Purchase Invoice (`Finance Review -> Finance Manager`). **Resolution:** We will implement Frappe Workflows for Material Request and Purchase Invoice matching the PDF exact states.")
    P("2. **In-Transit Handling:** Both documents emphasize 'In Transit' items, but JK-Workflow explicitly requires 'Packing -> Dispatch -> In Transit -> Branch Receiving'. **Resolution:** We will implement Custom Transit Warehouses and multi-step Stock Entries (Material Transfer) to strictly track items in transit.")
    P("3. **Daily Closing Verification:** Scope mentions basic cash closing. JK-Workflow adds 'Stock Verification' and 'Variance Investigation' to the Daily Branch Closing Flow. **Resolution:** The POS Closing process will be customized to require a Stock Reconciliation check before Branch Manager Approval.")
    P("4. **Warehouse Workflow:** JK-Workflow specifies a detailed Receiving -> Sorting -> SKU Generation -> Barcode Generation. **Resolution:** Item/SKU creation will occur post-receiving into a 'Receiving Area' virtual warehouse before moving to 'Ready Stock'.")
    P()

Header()

# PHASE 1
H(1, "Phase 1: Project Setup")
H(2, "Module: Development Environment")
Feature("System Initialization", "Initialize the development ecosystem.", "Standard unconfigured bench", "Custom App creation", "Isolate customizations", "Environment misconfigurations", "Developer environment testing", "Automated setup script")
T({
    "id": "1.1", "title": "Create Custom App and Repository",
    "purpose": "Isolate all project customizations in a dedicated Frappe app.",
    "req_ref": "Doc 1 (Scope): ERP Configuration", "flow_ref": "None",
    "desc": "Initialize `jahan_kodak` custom app and link it to GitHub.",
    "tech": {"module": "Core", "doctype": "None", "py": "hooks.py updates"},
    "impact": {}, "pm": {"deps": "None", "complexity": "Low", "time": "2 Hours"},
    "qa": {"acceptance": ["App created successfully", "Installed on site", "Pushed to GitHub"], "manual": ["bench new-app jahan_kodak", "bench --site site1.local install-app jahan_kodak"], "edge": [], "regression": []},
    "subtasks": ["Create app", "Configure hooks.py", "Initialize Git repo", "Push to GitHub branch 'develop'"]
})

# PHASE 2
H(1, "Phase 2: Core Configuration & Master Data")
H(2, "Module: Company & Organization")
Feature("Multi-Branch Architecture", "Company owns multiple branches with independent POS, Cash, and Warehouses.", "Branches are just standard Cost Centers/Warehouses", "Enforce branch-level isolation for cost centers, warehouses, and POS", "Requirement for independent branch profitability", "Data leakage between branches", "Role-based testing per branch", "Export fixtures for standard records")
T({
    "id": "2.1", "title": "Define Company and Base Hierarchy",
    "purpose": "Setup the root company and initial accounting structure.",
    "req_ref": "Scope 1.1", "flow_ref": "None",
    "desc": "Create Company 'Jahan Kodak'. Configure Base Currency.",
    "tech": {"module": "Setup", "doctype": "Company"},
    "impact": {"acc": "Sets base currency and defaults"}, "pm": {"deps": "1.1", "complexity": "Low", "time": "1 Hour"},
    "qa": {"acceptance": ["Company created"], "manual": ["Check company doctype"], "edge": [], "regression": []},
    "subtasks": ["Create Company", "Set default accounts"]
})
T({
    "id": "2.2", "title": "Create Branches",
    "purpose": "Create branch records for each store.",
    "req_ref": "Scope 1.2", "flow_ref": "Workflow 1. Procurement (Branch Operations)",
    "desc": "Create standard Branches: Kabul Center, Shahr-e-Naw, Karteh Naw, Macroyan, Dasht-e-Barchi.",
    "tech": {"module": "Setup", "doctype": "Branch"},
    "impact": {"acc": "Used for dimension filtering"}, "pm": {"deps": "2.1", "complexity": "Low", "time": "2 Hours"},
    "qa": {"acceptance": ["All branches exist"], "manual": ["List view shows all branches"], "edge": [], "regression": []},
    "subtasks": ["Create Kabul Branches", "Create Branch Cost Centers"]
})

# PHASE 3
H(1, "Phase 3: Inventory & Warehouses")
H(2, "Module: Warehouse Tree")
Feature("Centralized & Branch Warehouses", "Hierarchy of Central Warehouse -> Branch Warehouses.", "Standard Tree", "Define exact tree structure including Receiving and Transit", "Inventory isolation and transit tracking", "Wrong warehouse selection", "Stock balance tests", "Fixtures")
T({
    "id": "3.1", "title": "Create Warehouse Hierarchy (Including Transit & Receiving)",
    "purpose": "Setup Central, Receiving, Transit, and Branch warehouses.",
    "req_ref": "Scope 1.3", "flow_ref": "Workflow 2 & 3",
    "desc": "Create Central Warehouse (Parent). Create 'Receiving Area' Warehouse. Create 'In Transit' Warehouse. Create Branch Warehouses.",
    "tech": {"module": "Stock", "doctype": "Warehouse"},
    "impact": {"stock": "Base for all stock ledgers"}, "pm": {"deps": "2.2", "complexity": "Low", "time": "2 Hours"},
    "qa": {"acceptance": ["Tree view matches workflow doc"], "manual": ["View Warehouse Tree"], "edge": [], "regression": []},
    "subtasks": ["Create Central WH", "Create Receiving Area WH", "Create In Transit WH", "Create Branch WHs"]
})
H(2, "Module: SKU & Attributes")
Feature("Dynamic SKU & Barcodes", "Items need attributes (Size, Color, Brand) and auto-generated SKUs after receiving.", "SKUs are manual", "Auto generate SKU based on Category, Color, Size, Brand.", "Standardization of 1000s of items per Workflow 2", "SKU collision", "Test item creation", "Fixture export for Item Templates")
T({
    "id": "3.2", "title": "Define Item Attributes",
    "purpose": "Setup all variants for clothing.",
    "req_ref": "Scope 2.3", "flow_ref": "Workflow 2",
    "desc": "Create Item Attributes: Size, Color, Brand, Season.",
    "tech": {"module": "Stock", "doctype": "Item Attribute"},
    "impact": {"stock": "Defines variant combinations"}, "pm": {"deps": "2.1", "complexity": "Low", "time": "2 Hours"},
    "qa": {"acceptance": ["Attributes created"], "manual": ["Check Item Attribute list"], "edge": [], "regression": []},
    "subtasks": ["Create Size attribute", "Create Color attribute", "Create Brand attribute"]
})
T({
    "id": "3.3", "title": "Automated SKU & Barcode Generator",
    "purpose": "Generate SKU & Barcode automatically during sorting.",
    "req_ref": "Scope 2.1", "flow_ref": "Workflow 2",
    "desc": "Implement Server Script to generate SKU. Create Print Format for Label Printing.",
    "tech": {"module": "Stock", "doctype": "Item", "server": "Before Save", "print": "Barcode Label"},
    "impact": {"stock": "Item ID is auto-set"}, "pm": {"deps": "3.2", "complexity": "Medium", "time": "4 Hours"},
    "qa": {"acceptance": ["SKU auto-generated", "Label prints"], "manual": ["Create item variant", "Print label"], "edge": [], "regression": []},
    "subtasks": ["Add Abbreviation logic", "Write Python hook for `autoname`", "Create Print Format"]
})
T({
    "id": "3.4", "title": "Branch Replenishment Workflow",
    "purpose": "Manage branch restocks with transit.",
    "req_ref": "Scope 1.5", "flow_ref": "Workflow 3",
    "desc": "Stock Transfer Request -> Warehouse Approval -> Dispatch (Stock Entry to Transit) -> Branch Receiving (Stock Entry to Branch).",
    "tech": {"module": "Workflow", "doctype": "Material Request", "workflows": "Replenishment Workflow"},
    "impact": {"stock": "Tracks in-transit stock"}, "pm": {"deps": "3.1", "complexity": "High", "time": "6 Hours"},
    "qa": {"acceptance": ["Flow matches JK-Workflow 3"], "manual": ["Create transfer request", "Approve", "Dispatch", "Receive"], "edge": ["Partial receipt"], "regression": []},
    "subtasks": ["Create Workflow for Material Request", "Create Custom Button 'Dispatch to Transit'", "Create Custom Button 'Receive at Branch'"]
})

# PHASE 4
H(1, "Phase 4: Procurement")
H(2, "Module: Purchasing Cycle")
Feature("Strict Procurement Workflow", "Multi-stage approvals for MR and Cargo tracking.", "Standard Buying", "Implement workflows for MR and track Cargo transit.", "Workflow requirement", "Stuck approvals", "End-to-End procurement testing", "Custom Scripts")
T({
    "id": "4.1", "title": "Material Request Approval Workflow",
    "purpose": "Enforce Branch Manager and Procurement Approval.",
    "req_ref": "Scope 4", "flow_ref": "Workflow General Approvals",
    "desc": "Create Workflow on Material Request: Pending -> Branch Manager Approval -> Procurement Approval -> Approved.",
    "tech": {"module": "Workflow", "doctype": "Material Request"},
    "impact": {}, "pm": {"deps": "2.2", "complexity": "Low", "time": "2 Hours"},
    "qa": {"acceptance": ["Requires both approvals to proceed to PO"], "manual": ["Submit MR, approve twice"], "edge": ["Reject"], "regression": []},
    "subtasks": ["Define Workflow States", "Assign Roles"]
})
T({
    "id": "4.2", "title": "Purchase Order to Cargo Receive",
    "purpose": "Track Goods Shipped by Cargo.",
    "req_ref": "Scope 4", "flow_ref": "Workflow 1",
    "desc": "PO -> Goods Shipped (Custom Status) -> Receive at Main Warehouse (Purchase Receipt to 'Receiving Area').",
    "tech": {"module": "Buying", "doctype": "Purchase Order", "custom_fields": "Cargo Status"},
    "impact": {"stock": "Increases Receiving Area stock"}, "pm": {"deps": "4.1", "complexity": "Medium", "time": "4 Hours"},
    "qa": {"acceptance": ["Can track cargo status"], "manual": ["Update cargo status", "Create PR"], "edge": [], "regression": []},
    "subtasks": ["Add Cargo Tracking fields to PO", "Configure PR to land in Receiving Area"]
})

# PHASE 5
H(1, "Phase 5: Manufacturing")
H(2, "Module: Internal Production")
Feature("Apparel Manufacturing", "Produce clothing from raw materials.", "Standard ERPNext Manufacturing.", "Configure BOMs and Production Orders.", "Scope requirement", "Incorrect cost rollups", "BOM testing", "Fixtures")
T({
    "id": "5.1", "title": "Define Raw Materials and BOM",
    "purpose": "Setup BOMs for clothing items.",
    "req_ref": "Scope 5", "flow_ref": "None",
    "desc": "Define raw materials. Create BOMs for Finished Goods.",
    "tech": {"module": "Manufacturing", "doctype": "BOM"},
    "impact": {"stock": "Consumes raw, outputs finished"}, "pm": {"deps": "3.2", "complexity": "Medium", "time": "4 Hours"},
    "qa": {"acceptance": ["BOM correctly calculates cost"], "manual": ["Create BOM"], "edge": [], "regression": []},
    "subtasks": ["Create Raw Material Item Groups", "Create sample BOM", "Add Operations"]
})
T({
    "id": "5.2", "title": "Production Work Order Flow",
    "purpose": "Execute production.",
    "req_ref": "Scope 5", "flow_ref": "None",
    "desc": "Work Order -> Stock Entry (Transfer) -> Stock Entry (Manufacture).",
    "tech": {"module": "Manufacturing", "doctype": "Work Order"},
    "impact": {"stock": "Finished goods added to stock"}, "pm": {"deps": "5.1", "complexity": "Low", "time": "2 Hours"},
    "qa": {"acceptance": ["Work Order completes successfully"], "manual": ["Process full Work Order"], "edge": [], "regression": []},
    "subtasks": ["Test Work Order creation", "Validate final item cost"]
})

# PHASE 6
H(1, "Phase 6: POS & Sales")
H(2, "Module: POS Operations")
Feature("Multi-Register POS and Returns", "POS with barcode scan, multi-payment, and returns.", "Standard POS", "Configure POS Profiles, Return Workflows.", "Workflow 4 & 5", "Cash mismatch", "POS testing", "Fixtures")
T({
    "id": "6.1", "title": "POS Profiles and Multi-Payment",
    "purpose": "Setup POS for branches with Cash/Bank/Mobile Money.",
    "req_ref": "Scope 1.4", "flow_ref": "Workflow 4",
    "desc": "Create POS Profiles. Assign Warehouses. Add Payment Methods: Cash, Bank Card, Mobile Money.",
    "tech": {"module": "Retail", "doctype": "POS Profile"},
    "impact": {"acc": "Routes income and cash"}, "pm": {"deps": "3.1", "complexity": "Medium", "time": "4 Hours"},
    "qa": {"acceptance": ["Can split payment across methods"], "manual": ["Make mixed payment sale"], "edge": [], "regression": []},
    "subtasks": ["Create POS Profiles", "Configure Payment Methods"]
})
T({
    "id": "6.2", "title": "Customer Return Approval Workflow",
    "purpose": "Refund requires approval.",
    "req_ref": "Scope 6", "flow_ref": "Workflow 5",
    "desc": "Create Workflow for POS Return Invoice: Pending -> Refund Approval -> Approved (Updates Stock & Accounts).",
    "tech": {"module": "Workflow", "doctype": "Sales Invoice (Is Return)"},
    "impact": {"stock": "Returns to branch stock", "acc": "Reverses revenue"}, "pm": {"deps": "6.1", "complexity": "Medium", "time": "3 Hours"},
    "qa": {"acceptance": ["Return requires approval to post GL"], "manual": ["Create return, check GL"], "edge": [], "regression": []},
    "subtasks": ["Configure Sales Invoice Return Workflow", "Test stock impact on approval"]
})

# PHASE 7
H(1, "Phase 7: CRM & Loyalty")
H(2, "Module: Loyalty Program")
Feature("Customer Loyalty", "Loyalty program for wholesale customers.", "Standard Loyalty Program.", "Configure Loyalty Program.", "Scope 7", "Wrong discount", "Checkout testing", "Fixtures")
T({
    "id": "7.1", "title": "Configure Customer Loyalty",
    "purpose": "Award points for purchases.",
    "req_ref": "Scope 7", "flow_ref": "None",
    "desc": "Create Loyalty Program. Set point redemption rules.",
    "tech": {"module": "Retail", "doctype": "Loyalty Program"},
    "impact": {"acc": "Expense account for loyalty"}, "pm": {"deps": "6.1", "complexity": "Medium", "time": "3 Hours"},
    "qa": {"acceptance": ["Points awarded and redeemed"], "manual": ["Make sale, check points"], "edge": [], "regression": []},
    "subtasks": ["Setup Loyalty Program", "Setup Loyalty Expense Account"]
})

# PHASE 8
H(1, "Phase 8: Financial Management")
H(2, "Module: AP, AR & Daily Closing")
Feature("Daily Closing and Finance Approvals", "Strict closing with stock verification and PI payment approvals.", "Standard Accounts", "Setup COA, Closing workflow with Stock Recon, PI Workflow.", "Workflow 6 & 8", "Reconciliation errors", "Balance testing", "Fixtures")
T({
    "id": "8.1", "title": "Implement Chart of Accounts",
    "purpose": "Map to Afghan retail requirements.",
    "req_ref": "Scope Accounting", "flow_ref": "Workflow 6",
    "desc": "Create COA: Cash, Bank, AR, AP, Sales, COGS, Expenses.",
    "tech": {"module": "Accounts", "doctype": "Account"},
    "impact": {"acc": "Core structure"}, "pm": {"deps": "2.1", "complexity": "Medium", "time": "3 Hours"},
    "qa": {"acceptance": ["COA created"], "manual": ["Review Tree view"], "edge": [], "regression": []},
    "subtasks": ["Create Accounts"]
})
T({
    "id": "8.2", "title": "Purchase Invoice Finance Approval Workflow",
    "purpose": "Finance Manager must approve PI before payment.",
    "req_ref": "Scope Accounting", "flow_ref": "Workflow General Approvals",
    "desc": "Create Workflow on Purchase Invoice: Pending -> Finance Review -> Finance Manager Approval -> Unpaid/Payable.",
    "tech": {"module": "Workflow", "doctype": "Purchase Invoice"},
    "impact": {"acc": "Delays GL posting until approved"}, "pm": {"deps": "8.1", "complexity": "Medium", "time": "3 Hours"},
    "qa": {"acceptance": ["PI requires finance approval"], "manual": ["Submit PI"], "edge": [], "regression": []},
    "subtasks": ["Define Workflow", "Assign Roles"]
})
T({
    "id": "8.3", "title": "Daily Branch Closing with Stock Verification",
    "purpose": "Reconcile daily branch POS and Stock.",
    "req_ref": "Scope Accounting", "flow_ref": "Workflow 8",
    "desc": "Customize POS Closing Entry to require a link to a Stock Reconciliation document. Add 'Branch Manager Approval' workflow state.",
    "tech": {"module": "Retail", "doctype": "POS Closing Entry", "custom_fields": "Stock Recon Ref"},
    "impact": {"acc": "Consolidates POS invoices to Ledger"}, "pm": {"deps": "6.1", "complexity": "High", "time": "6 Hours"},
    "qa": {"acceptance": ["Cannot close without stock recon"], "manual": ["Run POS shift, close shift"], "edge": ["Stock variance handling"], "regression": []},
    "subtasks": ["Add Stock Recon link field to POS Closing", "Add Validation Script", "Add Workflow for Branch Manager Approval"]
})

# PHASE 9
H(1, "Phase 9: Human Resources")
H(2, "Module: HRMS")
Feature("Employee Management & Payroll Approval", "Recruitment, Attendance, Payroll with dual approvals.", "Standard HRMS", "Install HRMS app and configure payroll workflow.", "Workflow 7 & General", "Payroll miscalculation", "Payroll testing", "None")
T({
    "id": "9.1", "title": "Install and Configure HRMS",
    "purpose": "Manage Employees and Attendance.",
    "req_ref": "Scope 8", "flow_ref": "Workflow 7",
    "desc": "Install Frappe HR. Setup Employee master, Attendance, Leave Management.",
    "tech": {"module": "HR", "doctype": "Employee"},
    "impact": {"hr": "Full employee management"}, "pm": {"deps": "1.1", "complexity": "Medium", "time": "4 Hours"},
    "qa": {"acceptance": ["Employee records created", "Attendance recorded"], "manual": ["Mark attendance"], "edge": [], "regression": []},
    "subtasks": ["Install HRMS", "Configure Leave", "Configure Shifts"]
})
T({
    "id": "9.2", "title": "Payroll Processing & Approval Workflow",
    "purpose": "Process salary with HR and Finance approvals.",
    "req_ref": "Scope 8", "flow_ref": "Workflow General Approvals",
    "desc": "Configure Salary Structures. Create Workflow on Salary Slip/Payroll Entry: Pending -> HR Approval -> Finance Approval -> Paid.",
    "tech": {"module": "HR", "doctype": "Payroll Entry", "workflows": "Payroll Approval"},
    "impact": {"acc": "Hits payroll expense upon Finance Approval"}, "pm": {"deps": "9.1", "complexity": "High", "time": "5 Hours"},
    "qa": {"acceptance": ["Payroll requires dual approval"], "manual": ["Generate payroll, approve"], "edge": [], "regression": []},
    "subtasks": ["Setup Salary Components", "Create Workflow"]
})

# PHASE 10
H(1, "Phase 10: Reports & Dashboards")
H(2, "Module: Custom Reporting")
Feature("Management Reports", "Custom reports for sales, stock, performance.", "Standard reports exist.", "Develop Script Reports.", "Workflow 9", "Slow queries", "Data testing", "Python/JS files")
T({
    "id": "10.1", "title": "Develop Management Reports",
    "purpose": "Provide required visibility.",
    "req_ref": "Scope 9", "flow_ref": "Workflow 9",
    "desc": "Create Reports: Branch Sales, Top Selling Items, Slow Moving Items, Inventory Valuation, Gross Profit, Branch Profitability, Supplier Performance, Employee Performance.",
    "tech": {"module": "Custom", "doctype": "Report"},
    "impact": {}, "pm": {"deps": "8.1", "complexity": "High", "time": "12 Hours"},
    "qa": {"acceptance": ["All reports exist and accurate"], "manual": ["Run each report"], "edge": [], "regression": []},
    "subtasks": ["Develop Branch Profitability", "Develop Employee Performance", "Develop Top Selling/Slow Moving"]
})

# PHASE 11
H(1, "Phase 11: Data Migration & UAT")
H(2, "Module: Go-Live Prep")
Feature("Data Import & Testing", "Import legacy data and test.", "Data Import Tool", "Prepare templates and test scenarios.", "Scope 10, 12", "Corrupted data", "Balance validation", "None")
T({
    "id": "11.1", "title": "Import Master Data & Opening Balances",
    "purpose": "Load legacy data.",
    "req_ref": "Scope 10", "flow_ref": "None",
    "desc": "Import Items, Customers, Suppliers, Opening Stock, Opening Financial Balances.",
    "tech": {"module": "Data Import", "doctype": "Various"},
    "impact": {"acc": "Opening GL balances", "stock": "Opening Stock ledger"}, "pm": {"deps": "10.1", "complexity": "High", "time": "16 Hours"},
    "qa": {"acceptance": ["Trial balance matches legacy system"], "manual": ["Check TB"], "edge": [], "regression": []},
    "subtasks": ["Import Items", "Import Customers", "Import Suppliers", "Import Stock", "Import Accounts"]
})
T({
    "id": "11.2", "title": "User Acceptance Testing (UAT)",
    "purpose": "Validate workflows.",
    "req_ref": "Scope 12", "flow_ref": "All Workflows",
    "desc": "Execute end-to-end testing of Procurement, Main Warehouse Sorting/SKU, Branch Replenishment, POS Sales, Returns, Daily Closing, and Payroll approvals.",
    "tech": {"module": "All"},
    "impact": {}, "pm": {"deps": "11.1", "complexity": "High", "time": "24 Hours"},
    "qa": {"acceptance": ["All UAT signed off"], "manual": ["Run UAT scenarios with client"], "edge": [], "regression": []},
    "subtasks": ["Execute Procurement UAT", "Execute Warehouse UAT", "Execute POS UAT", "Execute HR UAT"]
})
T({
    "id": "11.3", "title": "Production Deployment",
    "purpose": "Go-Live.",
    "req_ref": "Scope 12", "flow_ref": "None",
    "desc": "Deploy to production server, train staff, commence support.",
    "tech": {"module": "Deployment"},
    "impact": {}, "pm": {"deps": "11.2", "complexity": "High", "time": "16 Hours"},
    "qa": {"acceptance": ["System live"], "manual": [], "edge": [], "regression": []},
    "subtasks": ["Setup Production Server", "Deploy Custom App", "Conduct Training"]
})

with open('/home/anonymous/projects/erp_next/docs/ERPNext_Implementation_Plan.md', 'w') as f:
    f.write('\n'.join(md))

print("Plan v2 generated successfully.")
