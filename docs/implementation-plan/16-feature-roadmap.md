# 16. Feature Roadmap & Master Backlog

This document maps out the 10-phase project backlog.

---

## Master Backlog Mapping

### Phase 1 - Foundation
*   **FND-01: Company & Branch Setup**
    *   *Description:* Define Company structure and Kabul, Mazar, Herat branches.
    *   *Dependencies:* None
    *   *Acceptance Criteria:* Branches show in HR lists and can be assigned to employees.
    *   *Modules:* HR, Core
    *   *Files Impacted:* None (Configuration)
    *   *Status:* NOT_STARTED
*   **FND-02: Cost Center Setup**
    *   *Description:* Configure branch-level cost center nodes in Chart of Accounts.
    *   *Dependencies:* FND-01
    *   *Acceptance Criteria:* Financial transactions can be filtered by Cost Center.
    *   *Modules:* Accounts
    *   *Files Impacted:* None (Configuration)
    *   *Status:* NOT_STARTED
*   **FND-03: Warehouse Tree Config**
    *   *Description:* Setup central and branch warehouses in a hierarchical structure.
    *   *Dependencies:* FND-01
    *   *Acceptance Criteria:* Stock entries can select parent city groups or child warehouses.
    *   *Modules:* Stock
    *   *Files Impacted:* None (Configuration)
    *   *Status:* NOT_STARTED
*   **FND-04: Chart of Accounts Setup**
    *   *Description:* Define assets, cash, bank, receivables, and expenses.
    *   *Dependencies:* FND-02
    *   *Acceptance Criteria:* Balanced transactions can be posted to new accounts.
    *   *Modules:* Accounts
    *   *Files Impacted:* None (Configuration)
    *   *Status:* NOT_STARTED
*   **FND-05: User Roles & Permissions**
    *   *Description:* Apply role access controls (Cashier, Warehouse Keeper, Accountant).
    *   *Dependencies:* None
    *   *Acceptance Criteria:* Users are restricted to their defined actions.
    *   *Modules:* Core
    *   *Files Impacted:* None (Configuration)
    *   *Status:* NOT_STARTED
*   **FND-06: Custom Login Page Customization**
    *   *Description:* Enhance web login page with modern custom glassmorphism and background animations.
    *   *Dependencies:* None
    *   *Acceptance Criteria:* Page displays layout correctly and overrides standard Frappe styles.
    *   *Modules:* Website
    *   *Files Impacted:* `/apps/ziad_app/ziad_app/hooks.py`, `/apps/ziad_app/ziad_app/public/css/ziad_app.css`, `/apps/ziad_app/ziad_app/public/js/ziad_app.js`
    *   *Status:* **COMPLETED** (Audited and verified in codebase)

---

### Phase 2 - Product Structure
*   **PRD-01: Item Groups & Attributes**
    *   *Description:* Define Clothing sizes, colors, and models.
    *   *Dependencies:* None
    *   *Acceptance Criteria:* Items can list size and color choices.
    *   *Modules:* Stock
    *   *Files Impacted:* None (Configuration)
    *   *Status:* NOT_STARTED
*   **PRD-02: Item Templates & Variants**
    *   *Description:* Create template items and auto-generate variant combinations.
    *   *Dependencies:* PRD-01
    *   *Acceptance Criteria:* Child item records generate automatically inside Item List.
    *   *Modules:* Stock
    *   *Files Impacted:* None (Configuration)
    *   *Status:* NOT_STARTED
*   **PRD-03: Variant SKU Naming Hook**
    *   *Description:* Implement code to auto-compile SKU name from attributes on save.
    *   *Dependencies:* PRD-02
    *   *Acceptance Criteria:* SKU shows exact format, e.g. `TSH-2026-BLK-L`.
    *   *Modules:* Stock, Custom App
    *   *Files Impacted:* `ziad_app/ziad_app/hooks.py`, `ziad_app/ziad_app/ziad_app/item.py`
    *   *Status:* NOT_STARTED
*   **PRD-04: Barcode Strategy Setup**
    *   *Description:* Map SKU codes to Item Barcodes and configure printable labels.
    *   *Dependencies:* PRD-03
    *   *Acceptance Criteria:* Item labels can render barcodes/QR codes correctly.
    *   *Modules:* Stock
    *   *Files Impacted:* Custom HTML Print Formats
    *   *Status:* NOT_STARTED

---

### Phase 3 - Inventory
*   **INV-01: Inter-Warehouse Transfers**
    *   *Description:* Setup Stock Entry workflows for moving items between central and branches.
    *   *Dependencies:* FND-03
    *   *Acceptance Criteria:* Stock balances adjust correctly across warehouses.
    *   *Modules:* Stock
    *   *Files Impacted:* None (Configuration)
    *   *Status:* NOT_STARTED
*   **INV-02: Auto Reorder & Safety Stock**
    *   *Description:* Define minimum stock warning levels.
    *   *Dependencies:* PRD-02
    *   *Acceptance Criteria:* Material Requests trigger automatically when stock falls below limits.
    *   *Modules:* Stock
    *   *Files Impacted:* None (Configuration)
    *   *Status:* NOT_STARTED
*   **INV-03: Batch Tracking**
    *   *Description:* Enable batch tracing for tracking production runs.
    *   *Dependencies:* PRD-02
    *   *Acceptance Criteria:* Items can be tracked by batch numbers at receipt and sale.
    *   *Modules:* Stock
    *   *Files Impacted:* None (Configuration)
    *   *Status:* NOT_STARTED

---

### Phase 4 - Procurement
*   **PRO-01: Requisition and RFQ Link**
    *   *Description:* Code custom button to quickly create RFQ from Material Request.
    *   *Dependencies:* None
    *   *Acceptance Criteria:* Button creates RFQ and populates all items automatically.
    *   *Modules:* Purchasing, Custom App
    *   *Files Impacted:* `ziad_app/ziad_app/public/js/material_request.js`
    *   *Status:* NOT_STARTED
*   **PRO-02: Cargo/In-Transit Flow**
    *   *Description:* Setup virtual transit warehouses and track ocean/air voyages.
    *   *Dependencies:* FND-03
    *   *Acceptance Criteria:* Stock can reside in transit status until receipt.
    *   *Modules:* Stock, Purchasing
    *   *Files Impacted:* None (Configuration)
    *   *Status:* NOT_STARTED
*   **PRO-03: Purchase Flow & Vendor Advances**
    *   *Description:* Configure payment entries linked to PO for advance tracking.
    *   *Dependencies:* FND-04
    *   *Acceptance Criteria:* Accounts payable ledger tracks net supplier balances correctly.
    *   *Modules:* Purchasing, Accounts
    *   *Files Impacted:* None (Configuration)
    *   *Status:* NOT_STARTED

---

### Phase 5 - Manufacturing
*   **MFG-01: Manufacturing BOM Config**
    *   *Description:* Define raw materials and operations for garment templates.
    *   *Dependencies:* PRD-02
    *   *Acceptance Criteria:* BOM calculates total unit production costs correctly.
    *   *Modules:* Manufacturing
    *   *Files Impacted:* None (Configuration)
    *   *Status:* NOT_STARTED
*   **MFG-02: Production Work Orders**
    *   *Description:* Setup Work Orders for releasing production to tailors/factories.
    *   *Dependencies:* MFG-01
    *   *Acceptance Criteria:* Work Order triggers material requirements from stock.
    *   *Modules:* Manufacturing
    *   *Files Impacted:* None (Configuration)
    *   *Status:* NOT_STARTED
*   **MFG-03: Raw Material Consumption**
    *   *Description:* Automate stock deduction of raw materials on finished goods receipt.
    *   *Dependencies:* MFG-02
    *   *Acceptance Criteria:* Finished garments increase, raw fabrics decrease in stock.
    *   *Modules:* Stock, Manufacturing
    *   *Files Impacted:* None (Configuration)
    *   *Status:* NOT_STARTED

---

### Phase 6 - POS (Point of Sale)
*   **POS-01: POS Profiles & Cashiers**
    *   *Description:* Configure POS profiles for retail outlets and cash float limits.
    *   *Dependencies:* FND-03
    *   *Acceptance Criteria:* POS cashier terminals can open shifts.
    *   *Modules:* Point of Sale
    *   *Files Impacted:* None (Configuration)
    *   *Status:* NOT_STARTED
*   **POS-02: Scanner Hardware Configuration**
    *   *Description:* Connect scanners and verify keyboard emulation entries.
    *   *Dependencies:* POS-01, PRD-04
    *   *Acceptance Criteria:* Scanning item barcode loads item instantly.
    *   *Modules:* Point of Sale
    *   *Files Impacted:* None (Hardware Setup)
    *   *Status:* NOT_STARTED
*   **POS-03: Cashier Shift Management**
    *   *Description:* Setup opening and closing shift reconciliations.
    *   *Dependencies:* POS-01
    *   *Acceptance Criteria:* Difference reports compare cash in hand with system sales logs.
    *   *Modules:* Point of Sale
    *   *Files Impacted:* None (Configuration)
    *   *Status:* NOT_STARTED

---

### Phase 7 - Customer Loyalty
*   **LOY-01: Tiers & Loyalty Setup**
    *   *Description:* Define customer groups and basic point reward programs.
    *   *Dependencies:* None
    *   *Acceptance Criteria:* Customer profiles track active point balances.
    *   *Modules:* Accounts, Custom App
    *   *Files Impacted:* None (Configuration)
    *   *Status:* NOT_STARTED
*   **LOY-02: Rolling Volume Scheduler Script**
    *   *Description:* Code daily background job to calculate 6/12 month customer spend and apply discount tiers.
    *   *Dependencies:* LOY-01
    *   *Acceptance Criteria:* Customers automatically update to 2.5% and 5% pricing rules on reaching target spend.
    *   *Modules:* Accounts, Custom App
    *   *Files Impacted:* `ziad_app/ziad_app/hooks.py`, `ziad_app/ziad_app/ziad_app/tasks.py`
    *   *Status:* NOT_STARTED

---

### Phase 8 - HRMS & Payroll
*   **HRM-01: Employee Database**
    *   *Description:* Populate employee profiles and branch mapping.
    *   *Dependencies:* FND-01
    *   *Acceptance Criteria:* Staff records show correct city branch references.
    *   *Modules:* HRMS
    *   *Files Impacted:* None (Configuration)
    *   *Status:* NOT_STARTED
*   **HRM-02: Attendance and Leave Management**
    *   *Description:* Configure standard leave applications and attendance logs.
    *   *Dependencies:* HRM-01
    *   *Acceptance Criteria:* Employees can log daily check-ins.
    *   *Modules:* HRMS
    *   *Files Impacted:* None (Configuration)
    *   *Status:* NOT_STARTED
*   **HRM-03: Salary Structure & Payroll**
    *   *Description:* Configure tax slabs, allowances, and automatic monthly salary slip generation.
    *   *Dependencies:* HRM-01, FND-04
    *   *Acceptance Criteria:* Payroll processing outputs double-entry salary expense entries.
    *   *Modules:* HRMS, Accounts
    *   *Files Impacted:* None (Configuration)
    *   *Status:* NOT_STARTED

---

### Phase 9 - Reporting & Dashboards
*   **REP-01: Cost Center Branch Profitability**
    *   *Description:* Program custom script report mapping net branch margins (P&L).
    *   *Dependencies:* FND-02, FND-04
    *   *Acceptance Criteria:* Report calculates correct net profit per branch.
    *   *Modules:* Accounts, Custom App
    *   *Files Impacted:* Custom Report files in `ziad_app`
    *   *Status:* NOT_STARTED
*   **REP-02: Stock Turnover Analysis**
    *   *Description:* Build stock turnover query reports.
    *   *Dependencies:* INV-01
    *   *Acceptance Criteria:* Report displays correct ratios for fast/slow-moving inventory.
    *   *Modules:* Stock
    *   *Files Impacted:* None (Configuration Report Builder)
    *   *Status:* NOT_STARTED

---

### Phase 10 - E-Commerce Integrations
*   **INT-01: Web APIs Setup**
    *   *Description:* Configure REST API tokens and link incoming order hooks.
    *   *Dependencies:* PRD-02, FND-04
    *   *Acceptance Criteria:* External POST request successfully logs sales order.
    *   *Modules:* Core, Custom App
    *   *Files Impacted:* API custom handlers
    *   *Status:* NOT_STARTED
