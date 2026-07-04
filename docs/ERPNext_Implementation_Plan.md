# ERPNext Implementation Master Roadmap: Jahan Kodak
This document serves as the single source of truth for the entire ERPNext customization project. Every developer must strictly follow this plan.

## Document Conflicts & Resolutions
During the analysis of the Scope Document (Doc 1) and JK-Workflow PDF (Doc 2), the following conflicts and refinements were identified:
1. **Procurement Approvals:** Doc 1 has a basic procurement flow. JK-Workflow requires multi-level approval for Material Request (`Branch Manager -> Procurement Approval`) and Purchase Invoice (`Finance Review -> Finance Manager`). **Resolution:** We will implement Frappe Workflows for Material Request and Purchase Invoice matching the PDF exact states.
2. **In-Transit Handling:** Both documents emphasize 'In Transit' items, but JK-Workflow explicitly requires 'Packing -> Dispatch -> In Transit -> Branch Receiving'. **Resolution:** We will implement Custom Transit Warehouses and multi-step Stock Entries (Material Transfer) to strictly track items in transit.
3. **Daily Closing Verification:** Scope mentions basic cash closing. JK-Workflow adds 'Stock Verification' and 'Variance Investigation' to the Daily Branch Closing Flow. **Resolution:** The POS Closing process will be customized to require a Stock Reconciliation check before Branch Manager Approval.
4. **Warehouse Workflow:** JK-Workflow specifies a detailed Receiving -> Sorting -> SKU Generation -> Barcode Generation. **Resolution:** Item/SKU creation will occur post-receiving into a 'Receiving Area' virtual warehouse before moving to 'Ready Stock'.

# Phase 1: Project Setup
## Module: Development Environment
### Feature: System Initialization
**Business Process:** Initialize the development ecosystem.
**Current ERPNext Behavior:** Standard unconfigured bench
**Required Customization:** Custom App creation
**Reason:** Isolate customizations
**Possible Risks:** Environment misconfigurations
**Testing Strategy:** Developer environment testing
**Deployment Strategy:** Automated setup script

#### Task 1.1: Create Custom App and Repository
**Status:** 🟩 Completed
**Purpose:** Isolate all project customizations in a dedicated Frappe app.
**Business Requirement Reference:** Doc 1 (Scope): ERP Configuration
**Workflow Reference:** None
**Description:** Initialize `jahan_kodak` custom app and link it to GitHub.

##### Technical Design
- **ERPNext Module:** Core
- **Doctype Changes:** None
- **Custom Fields:** None
- **Child Tables:** None
- **Server Scripts:** None
- **Client Scripts:** None
- **Python Files:** hooks.py updates
- **JS Files:** None
- **Print Formats:** None
- **Reports:** None
- **Permissions:** System Manager
- **Role Changes:** None
- **Workflow Changes:** None
- **Notification Changes:** None

##### Impact Analysis
- **Accounting Impact:** None
- **Stock Impact:** None
- **HR Impact:** None
- **API Impact:** None

##### Project Management
- **Dependencies:** None
- **Estimated Complexity:** Low
- **Estimated Time:** 2 Hours

##### Testing & Quality Assurance
**Acceptance Criteria:**
- App created successfully
- Installed on site
- Pushed to GitHub

**Manual Test Cases:**
- bench new-app jahan_kodak
- bench --site site1.local install-app jahan_kodak

**Edge Cases:**

**Regression Test Requirements:**

##### Subtasks
- [x] Create app
- [x] Configure hooks.py
- [x] Initialize Git repo
- [x] Push to GitHub branch 'develop'

##### GitHub Workflow & Deployment
- **Git Branch Name:** `feat/TASK-1-1`
- **Suggested Commit Message:** `feat: implement Create Custom App and Repository`
- **Production Deployment Notes:** Standard migration.
- **Rollback Strategy:** Git revert and restore database if necessary.
---

# Phase 2: Core Configuration & Master Data
## Module: Company & Organization
### Feature: Multi-Branch Architecture
**Business Process:** Company owns multiple branches with independent POS, Cash, and Warehouses.
**Current ERPNext Behavior:** Branches are just standard Cost Centers/Warehouses
**Required Customization:** Enforce branch-level isolation for cost centers, warehouses, and POS
**Reason:** Requirement for independent branch profitability
**Possible Risks:** Data leakage between branches
**Testing Strategy:** Role-based testing per branch
**Deployment Strategy:** Export fixtures for standard records

#### Task 2.1: Define Company and Base Hierarchy
**Status:** 🟩 Completed
**Purpose:** Setup the root company and initial accounting structure.
**Business Requirement Reference:** Scope 1.1
**Workflow Reference:** None
**Description:** Create Company 'Jahan Kodak'. Configure Base Currency.

##### Technical Design
- **ERPNext Module:** Setup
- **Doctype Changes:** Company
- **Custom Fields:** None
- **Child Tables:** None
- **Server Scripts:** None
- **Client Scripts:** None
- **Python Files:** None
- **JS Files:** None
- **Print Formats:** None
- **Reports:** None
- **Permissions:** System Manager
- **Role Changes:** None
- **Workflow Changes:** None
- **Notification Changes:** None

##### Impact Analysis
- **Accounting Impact:** Sets base currency and defaults
- **Stock Impact:** None
- **HR Impact:** None
- **API Impact:** None

##### Project Management
- **Dependencies:** 1.1
- **Estimated Complexity:** Low
- **Estimated Time:** 1 Hour

##### Testing & Quality Assurance
**Acceptance Criteria:**
- Company created

**Manual Test Cases:**
- Check company doctype

**Edge Cases:**

**Regression Test Requirements:**

##### Subtasks
- [x] Create Company
- [x] Set default accounts

##### GitHub Workflow & Deployment
- **Git Branch Name:** `feat/TASK-2-1`
- **Suggested Commit Message:** `feat: implement Define Company and Base Hierarchy`
- **Production Deployment Notes:** Standard migration.
- **Rollback Strategy:** Git revert and restore database if necessary.
---

#### Task 2.2: Create Branches
**Status:** 🟩 Completed
**Purpose:** Create branch records for each store.
**Business Requirement Reference:** Scope 1.2
**Workflow Reference:** Workflow 1. Procurement (Branch Operations)
**Description:** Create standard Branches: Kabul Center, Shahr-e-Naw, Karteh Naw, Macroyan, Dasht-e-Barchi.

##### Technical Design
- **ERPNext Module:** Setup
- **Doctype Changes:** Branch
- **Custom Fields:** None
- **Child Tables:** None
- **Server Scripts:** None
- **Client Scripts:** None
- **Python Files:** None
- **JS Files:** None
- **Print Formats:** None
- **Reports:** None
- **Permissions:** System Manager
- **Role Changes:** None
- **Workflow Changes:** None
- **Notification Changes:** None

##### Impact Analysis
- **Accounting Impact:** Used for dimension filtering
- **Stock Impact:** None
- **HR Impact:** None
- **API Impact:** None

##### Project Management
- **Dependencies:** 2.1
- **Estimated Complexity:** Low
- **Estimated Time:** 2 Hours

##### Testing & Quality Assurance
**Acceptance Criteria:**
- All branches exist

**Manual Test Cases:**
- List view shows all branches

**Edge Cases:**

**Regression Test Requirements:**

##### Subtasks
- [x] Create Kabul Branches
- [x] Create Branch Cost Centers

##### GitHub Workflow & Deployment
- **Git Branch Name:** `feat/TASK-2-2`
- **Suggested Commit Message:** `feat: implement Create Branches`
- **Production Deployment Notes:** Standard migration.
- **Rollback Strategy:** Git revert and restore database if necessary.
---

# Phase 3: Inventory & Warehouses
## Module: Warehouse Tree
### Feature: Centralized & Branch Warehouses
**Business Process:** Hierarchy of Central Warehouse -> Branch Warehouses.
**Current ERPNext Behavior:** Standard Tree
**Required Customization:** Define exact tree structure including Receiving and Transit
**Reason:** Inventory isolation and transit tracking
**Possible Risks:** Wrong warehouse selection
**Testing Strategy:** Stock balance tests
**Deployment Strategy:** Fixtures

#### Task 3.1: Create Warehouse Hierarchy (Including Transit & Receiving)
**Status:** 🟩 Completed
**Purpose:** Setup Central, Receiving, Transit, and Branch warehouses.
**Business Requirement Reference:** Scope 1.3
**Workflow Reference:** Workflow 2 & 3
**Description:** Create Central Warehouse (Parent). Create 'Receiving Area' Warehouse. Create 'In Transit' Warehouse. Create Branch Warehouses.

##### Technical Design
- **ERPNext Module:** Stock
- **Doctype Changes:** Warehouse
- **Custom Fields:** None
- **Child Tables:** None
- **Server Scripts:** None
- **Client Scripts:** None
- **Python Files:** None
- **JS Files:** None
- **Print Formats:** None
- **Reports:** None
- **Permissions:** System Manager
- **Role Changes:** None
- **Workflow Changes:** None
- **Notification Changes:** None

##### Impact Analysis
- **Accounting Impact:** None
- **Stock Impact:** Base for all stock ledgers
- **HR Impact:** None
- **API Impact:** None

##### Project Management
- **Dependencies:** 2.2
- **Estimated Complexity:** Low
- **Estimated Time:** 2 Hours

##### Testing & Quality Assurance
**Acceptance Criteria:**
- Tree view matches workflow doc

**Manual Test Cases:**
- View Warehouse Tree

**Edge Cases:**

**Regression Test Requirements:**

##### Subtasks
- [x] Create Central WH
- [x] Create Receiving Area WH
- [x] Create In Transit WH
- [x] Create Branch WHs

##### GitHub Workflow & Deployment
- **Git Branch Name:** `feat/TASK-3-1`
- **Suggested Commit Message:** `feat: implement Create Warehouse Hierarchy (Including Transit & Receiving)`
- **Production Deployment Notes:** Standard migration.
- **Rollback Strategy:** Git revert and restore database if necessary.
---

## Module: SKU & Attributes
### Feature: Dynamic SKU & Barcodes
**Business Process:** Items need attributes (Size, Color, Brand) and auto-generated SKUs after receiving.
**Current ERPNext Behavior:** SKUs are manual
**Required Customization:** Auto generate SKU based on Category, Color, Size, Brand.
**Reason:** Standardization of 1000s of items per Workflow 2
**Possible Risks:** SKU collision
**Testing Strategy:** Test item creation
**Deployment Strategy:** Fixture export for Item Templates

#### Task 3.2: Define Item Attributes
**Status:** 🟩 Completed
**Purpose:** Setup all variants for clothing.
**Business Requirement Reference:** Scope 2.3
**Workflow Reference:** Workflow 2
**Description:** Create Item Attributes: Size, Color, Brand, Season.

##### Technical Design
- **ERPNext Module:** Stock
- **Doctype Changes:** Item Attribute
- **Custom Fields:** None
- **Child Tables:** None
- **Server Scripts:** None
- **Client Scripts:** None
- **Python Files:** None
- **JS Files:** None
- **Print Formats:** None
- **Reports:** None
- **Permissions:** System Manager
- **Role Changes:** None
- **Workflow Changes:** None
- **Notification Changes:** None

##### Impact Analysis
- **Accounting Impact:** None
- **Stock Impact:** Defines variant combinations
- **HR Impact:** None
- **API Impact:** None

##### Project Management
- **Dependencies:** 2.1
- **Estimated Complexity:** Low
- **Estimated Time:** 2 Hours

##### Testing & Quality Assurance
**Acceptance Criteria:**
- Attributes created

**Manual Test Cases:**
- Check Item Attribute list

**Edge Cases:**

**Regression Test Requirements:**

##### Subtasks
- [x] Create Size attribute
- [x] Create Color attribute
- [x] Create Brand attribute

##### GitHub Workflow & Deployment
- **Git Branch Name:** `feat/TASK-3-2`
- **Suggested Commit Message:** `feat: implement Define Item Attributes`
- **Production Deployment Notes:** Standard migration.
- **Rollback Strategy:** Git revert and restore database if necessary.
---

#### Task 3.3: Automated SKU & Barcode Generator
**Status:** 🟩 Completed
**Purpose:** Generate SKU & Barcode automatically during sorting.
**Business Requirement Reference:** Scope 2.1
**Workflow Reference:** Workflow 2
**Description:** Implement Server Script to generate SKU. Create Print Format for Label Printing.

##### Technical Design
- **ERPNext Module:** Stock
- **Doctype Changes:** Item
- **Custom Fields:** None
- **Child Tables:** None
- **Server Scripts:** Before Save
- **Client Scripts:** None
- **Python Files:** None
- **JS Files:** None
- **Print Formats:** Barcode Label
- **Reports:** None
- **Permissions:** System Manager
- **Role Changes:** None
- **Workflow Changes:** None
- **Notification Changes:** None

##### Impact Analysis
- **Accounting Impact:** None
- **Stock Impact:** Item ID is auto-set
- **HR Impact:** None
- **API Impact:** None

##### Project Management
- **Dependencies:** 3.2
- **Estimated Complexity:** Medium
- **Estimated Time:** 4 Hours

##### Testing & Quality Assurance
**Acceptance Criteria:**
- SKU auto-generated
- Label prints

**Manual Test Cases:**
- Create item variant
- Print label

**Edge Cases:**

**Regression Test Requirements:**

##### Subtasks
- [x] Add Abbreviation logic
- [x] Write Python hook for `autoname`
- [x] Create Print Format

##### GitHub Workflow & Deployment
- **Git Branch Name:** `feat/TASK-3-3`
- **Suggested Commit Message:** `feat: implement Automated SKU & Barcode Generator`
- **Production Deployment Notes:** Standard migration.
- **Rollback Strategy:** Git revert and restore database if necessary.
---

#### Task 3.4: Branch Replenishment Workflow
**Status:** 🟩 Completed
**Purpose:** Manage branch restocks with transit.
**Business Requirement Reference:** Scope 1.5
**Workflow Reference:** Workflow 3
**Description:** Stock Transfer Request -> Warehouse Approval -> Dispatch (Stock Entry to Transit) -> Branch Receiving (Stock Entry to Branch).

##### Technical Design
- **ERPNext Module:** Workflow
- **Doctype Changes:** Material Request
- **Custom Fields:** None
- **Child Tables:** None
- **Server Scripts:** None
- **Client Scripts:** None
- **Python Files:** None
- **JS Files:** None
- **Print Formats:** None
- **Reports:** None
- **Permissions:** System Manager
- **Role Changes:** None
- **Workflow Changes:** Replenishment Workflow
- **Notification Changes:** None

##### Impact Analysis
- **Accounting Impact:** None
- **Stock Impact:** Tracks in-transit stock
- **HR Impact:** None
- **API Impact:** None

##### Project Management
- **Dependencies:** 3.1
- **Estimated Complexity:** High
- **Estimated Time:** 6 Hours

##### Testing & Quality Assurance
**Acceptance Criteria:**
- Flow matches JK-Workflow 3

**Manual Test Cases:**
- Create transfer request
- Approve
- Dispatch
- Receive

**Edge Cases:**
- Partial receipt

**Regression Test Requirements:**

##### Subtasks
- [x] Create Workflow for Material Request
- [x] Create Custom Button 'Dispatch to Transit'
- [x] Create Custom Button 'Receive at Branch'

##### GitHub Workflow & Deployment
- **Git Branch Name:** `feat/TASK-3-4`
- **Suggested Commit Message:** `feat: implement Branch Replenishment Workflow`
- **Production Deployment Notes:** Standard migration.
- **Rollback Strategy:** Git revert and restore database if necessary.
---

# Phase 4: Procurement
## Module: Purchasing Cycle
### Feature: Strict Procurement Workflow
**Business Process:** Multi-stage approvals for MR and Cargo tracking.
**Current ERPNext Behavior:** Standard Buying
**Required Customization:** Implement workflows for MR and track Cargo transit.
**Reason:** Workflow requirement
**Possible Risks:** Stuck approvals
**Testing Strategy:** End-to-End procurement testing
**Deployment Strategy:** Custom Scripts

#### Task 4.1: Material Request Approval Workflow
**Status:** 🟩 Completed
**Purpose:** Enforce Branch Manager and Procurement Approval.
**Business Requirement Reference:** Scope 4
**Workflow Reference:** Workflow General Approvals
**Description:** Create Workflow on Material Request: Pending -> Branch Manager Approval -> Procurement Approval -> Approved.

##### Technical Design
- **ERPNext Module:** Workflow
- **Doctype Changes:** Material Request
- **Custom Fields:** None
- **Child Tables:** None
- **Server Scripts:** None
- **Client Scripts:** None
- **Python Files:** None
- **JS Files:** None
- **Print Formats:** None
- **Reports:** None
- **Permissions:** System Manager
- **Role Changes:** None
- **Workflow Changes:** None
- **Notification Changes:** None

##### Impact Analysis
- **Accounting Impact:** None
- **Stock Impact:** None
- **HR Impact:** None
- **API Impact:** None

##### Project Management
- **Dependencies:** 2.2
- **Estimated Complexity:** Low
- **Estimated Time:** 2 Hours

##### Testing & Quality Assurance
**Acceptance Criteria:**
- Requires both approvals to proceed to PO

**Manual Test Cases:**
- Submit MR, approve twice

**Edge Cases:**
- Reject

**Regression Test Requirements:**

##### Subtasks
- [x] Define Workflow States
- [x] Assign Roles

##### GitHub Workflow & Deployment
- **Git Branch Name:** `feat/TASK-4-1`
- **Suggested Commit Message:** `feat: implement Material Request Approval Workflow`
- **Production Deployment Notes:** Standard migration.
- **Rollback Strategy:** Git revert and restore database if necessary.
---

#### Task 4.2: Purchase Order to Cargo Receive
**Status:** 🟩 Completed
**Purpose:** Track Goods Shipped by Cargo.
**Business Requirement Reference:** Scope 4
**Workflow Reference:** Workflow 1
**Description:** PO -> Goods Shipped (Custom Status) -> Receive at Main Warehouse (Purchase Receipt to 'Receiving Area').

##### Technical Design
- **ERPNext Module:** Buying
- **Doctype Changes:** Purchase Order
- **Custom Fields:** None
- **Child Tables:** None
- **Server Scripts:** None
- **Client Scripts:** None
- **Python Files:** None
- **JS Files:** None
- **Print Formats:** None
- **Reports:** None
- **Permissions:** System Manager
- **Role Changes:** None
- **Workflow Changes:** None
- **Notification Changes:** None

##### Impact Analysis
- **Accounting Impact:** None
- **Stock Impact:** Increases Receiving Area stock
- **HR Impact:** None
- **API Impact:** None

##### Project Management
- **Dependencies:** 4.1
- **Estimated Complexity:** Medium
- **Estimated Time:** 4 Hours

##### Testing & Quality Assurance
**Acceptance Criteria:**
- Can track cargo status

**Manual Test Cases:**
- Update cargo status
- Create PR

**Edge Cases:**

**Regression Test Requirements:**

##### Subtasks
- [x] Add Cargo Tracking fields to PO
- [x] Configure PR to land in Receiving Area

##### GitHub Workflow & Deployment
- **Git Branch Name:** `feat/TASK-4-2`
- **Suggested Commit Message:** `feat: implement Purchase Order to Cargo Receive`
- **Production Deployment Notes:** Standard migration.
- **Rollback Strategy:** Git revert and restore database if necessary.
---

# Phase 5: Manufacturing
## Module: Internal Production
### Feature: Apparel Manufacturing
**Business Process:** Produce clothing from raw materials.
**Current ERPNext Behavior:** Standard ERPNext Manufacturing.
**Required Customization:** Configure BOMs and Production Orders.
**Reason:** Scope requirement
**Possible Risks:** Incorrect cost rollups
**Testing Strategy:** BOM testing
**Deployment Strategy:** Fixtures

#### Task 5.1: Define Raw Materials and BOM
**Status:** ⬜ Not Started
**Purpose:** Setup BOMs for clothing items.
**Business Requirement Reference:** Scope 5
**Workflow Reference:** None
**Description:** Define raw materials. Create BOMs for Finished Goods.

##### Technical Design
- **ERPNext Module:** Manufacturing
- **Doctype Changes:** BOM
- **Custom Fields:** None
- **Child Tables:** None
- **Server Scripts:** None
- **Client Scripts:** None
- **Python Files:** None
- **JS Files:** None
- **Print Formats:** None
- **Reports:** None
- **Permissions:** System Manager
- **Role Changes:** None
- **Workflow Changes:** None
- **Notification Changes:** None

##### Impact Analysis
- **Accounting Impact:** None
- **Stock Impact:** Consumes raw, outputs finished
- **HR Impact:** None
- **API Impact:** None

##### Project Management
- **Dependencies:** 3.2
- **Estimated Complexity:** Medium
- **Estimated Time:** 4 Hours

##### Testing & Quality Assurance
**Acceptance Criteria:**
- BOM correctly calculates cost

**Manual Test Cases:**
- Create BOM

**Edge Cases:**

**Regression Test Requirements:**

##### Subtasks
- [ ] Create Raw Material Item Groups
- [ ] Create sample BOM
- [ ] Add Operations

##### GitHub Workflow & Deployment
- **Git Branch Name:** `feat/TASK-5-1`
- **Suggested Commit Message:** `feat: implement Define Raw Materials and BOM`
- **Production Deployment Notes:** Standard migration.
- **Rollback Strategy:** Git revert and restore database if necessary.
---

#### Task 5.2: Production Work Order Flow
**Status:** ⬜ Not Started
**Purpose:** Execute production.
**Business Requirement Reference:** Scope 5
**Workflow Reference:** None
**Description:** Work Order -> Stock Entry (Transfer) -> Stock Entry (Manufacture).

##### Technical Design
- **ERPNext Module:** Manufacturing
- **Doctype Changes:** Work Order
- **Custom Fields:** None
- **Child Tables:** None
- **Server Scripts:** None
- **Client Scripts:** None
- **Python Files:** None
- **JS Files:** None
- **Print Formats:** None
- **Reports:** None
- **Permissions:** System Manager
- **Role Changes:** None
- **Workflow Changes:** None
- **Notification Changes:** None

##### Impact Analysis
- **Accounting Impact:** None
- **Stock Impact:** Finished goods added to stock
- **HR Impact:** None
- **API Impact:** None

##### Project Management
- **Dependencies:** 5.1
- **Estimated Complexity:** Low
- **Estimated Time:** 2 Hours

##### Testing & Quality Assurance
**Acceptance Criteria:**
- Work Order completes successfully

**Manual Test Cases:**
- Process full Work Order

**Edge Cases:**

**Regression Test Requirements:**

##### Subtasks
- [ ] Test Work Order creation
- [ ] Validate final item cost

##### GitHub Workflow & Deployment
- **Git Branch Name:** `feat/TASK-5-2`
- **Suggested Commit Message:** `feat: implement Production Work Order Flow`
- **Production Deployment Notes:** Standard migration.
- **Rollback Strategy:** Git revert and restore database if necessary.
---

# Phase 6: POS & Sales
## Module: POS Operations
### Feature: Multi-Register POS and Returns
**Business Process:** POS with barcode scan, multi-payment, and returns.
**Current ERPNext Behavior:** Standard POS
**Required Customization:** Configure POS Profiles, Return Workflows.
**Reason:** Workflow 4 & 5
**Possible Risks:** Cash mismatch
**Testing Strategy:** POS testing
**Deployment Strategy:** Fixtures

#### Task 6.1: POS Profiles and Multi-Payment
**Status:** ⬜ Not Started
**Purpose:** Setup POS for branches with Cash/Bank/Mobile Money.
**Business Requirement Reference:** Scope 1.4
**Workflow Reference:** Workflow 4
**Description:** Create POS Profiles. Assign Warehouses. Add Payment Methods: Cash, Bank Card, Mobile Money.

##### Technical Design
- **ERPNext Module:** Retail
- **Doctype Changes:** POS Profile
- **Custom Fields:** None
- **Child Tables:** None
- **Server Scripts:** None
- **Client Scripts:** None
- **Python Files:** None
- **JS Files:** None
- **Print Formats:** None
- **Reports:** None
- **Permissions:** System Manager
- **Role Changes:** None
- **Workflow Changes:** None
- **Notification Changes:** None

##### Impact Analysis
- **Accounting Impact:** Routes income and cash
- **Stock Impact:** None
- **HR Impact:** None
- **API Impact:** None

##### Project Management
- **Dependencies:** 3.1
- **Estimated Complexity:** Medium
- **Estimated Time:** 4 Hours

##### Testing & Quality Assurance
**Acceptance Criteria:**
- Can split payment across methods

**Manual Test Cases:**
- Make mixed payment sale

**Edge Cases:**

**Regression Test Requirements:**

##### Subtasks
- [ ] Create POS Profiles
- [ ] Configure Payment Methods

##### GitHub Workflow & Deployment
- **Git Branch Name:** `feat/TASK-6-1`
- **Suggested Commit Message:** `feat: implement POS Profiles and Multi-Payment`
- **Production Deployment Notes:** Standard migration.
- **Rollback Strategy:** Git revert and restore database if necessary.
---

#### Task 6.2: Customer Return Approval Workflow
**Status:** ⬜ Not Started
**Purpose:** Refund requires approval.
**Business Requirement Reference:** Scope 6
**Workflow Reference:** Workflow 5
**Description:** Create Workflow for POS Return Invoice: Pending -> Refund Approval -> Approved (Updates Stock & Accounts).

##### Technical Design
- **ERPNext Module:** Workflow
- **Doctype Changes:** Sales Invoice (Is Return)
- **Custom Fields:** None
- **Child Tables:** None
- **Server Scripts:** None
- **Client Scripts:** None
- **Python Files:** None
- **JS Files:** None
- **Print Formats:** None
- **Reports:** None
- **Permissions:** System Manager
- **Role Changes:** None
- **Workflow Changes:** None
- **Notification Changes:** None

##### Impact Analysis
- **Accounting Impact:** Reverses revenue
- **Stock Impact:** Returns to branch stock
- **HR Impact:** None
- **API Impact:** None

##### Project Management
- **Dependencies:** 6.1
- **Estimated Complexity:** Medium
- **Estimated Time:** 3 Hours

##### Testing & Quality Assurance
**Acceptance Criteria:**
- Return requires approval to post GL

**Manual Test Cases:**
- Create return, check GL

**Edge Cases:**

**Regression Test Requirements:**

##### Subtasks
- [ ] Configure Sales Invoice Return Workflow
- [ ] Test stock impact on approval

##### GitHub Workflow & Deployment
- **Git Branch Name:** `feat/TASK-6-2`
- **Suggested Commit Message:** `feat: implement Customer Return Approval Workflow`
- **Production Deployment Notes:** Standard migration.
- **Rollback Strategy:** Git revert and restore database if necessary.
---

# Phase 7: CRM & Loyalty
## Module: Loyalty Program
### Feature: Customer Loyalty
**Business Process:** Loyalty program for wholesale customers.
**Current ERPNext Behavior:** Standard Loyalty Program.
**Required Customization:** Configure Loyalty Program.
**Reason:** Scope 7
**Possible Risks:** Wrong discount
**Testing Strategy:** Checkout testing
**Deployment Strategy:** Fixtures

#### Task 7.1: Configure Customer Loyalty
**Status:** ⬜ Not Started
**Purpose:** Award points for purchases.
**Business Requirement Reference:** Scope 7
**Workflow Reference:** None
**Description:** Create Loyalty Program. Set point redemption rules.

##### Technical Design
- **ERPNext Module:** Retail
- **Doctype Changes:** Loyalty Program
- **Custom Fields:** None
- **Child Tables:** None
- **Server Scripts:** None
- **Client Scripts:** None
- **Python Files:** None
- **JS Files:** None
- **Print Formats:** None
- **Reports:** None
- **Permissions:** System Manager
- **Role Changes:** None
- **Workflow Changes:** None
- **Notification Changes:** None

##### Impact Analysis
- **Accounting Impact:** Expense account for loyalty
- **Stock Impact:** None
- **HR Impact:** None
- **API Impact:** None

##### Project Management
- **Dependencies:** 6.1
- **Estimated Complexity:** Medium
- **Estimated Time:** 3 Hours

##### Testing & Quality Assurance
**Acceptance Criteria:**
- Points awarded and redeemed

**Manual Test Cases:**
- Make sale, check points

**Edge Cases:**

**Regression Test Requirements:**

##### Subtasks
- [ ] Setup Loyalty Program
- [ ] Setup Loyalty Expense Account

##### GitHub Workflow & Deployment
- **Git Branch Name:** `feat/TASK-7-1`
- **Suggested Commit Message:** `feat: implement Configure Customer Loyalty`
- **Production Deployment Notes:** Standard migration.
- **Rollback Strategy:** Git revert and restore database if necessary.
---

# Phase 8: Financial Management
## Module: AP, AR & Daily Closing
### Feature: Daily Closing and Finance Approvals
**Business Process:** Strict closing with stock verification and PI payment approvals.
**Current ERPNext Behavior:** Standard Accounts
**Required Customization:** Setup COA, Closing workflow with Stock Recon, PI Workflow.
**Reason:** Workflow 6 & 8
**Possible Risks:** Reconciliation errors
**Testing Strategy:** Balance testing
**Deployment Strategy:** Fixtures

#### Task 8.1: Implement Chart of Accounts
**Status:** ⬜ Not Started
**Purpose:** Map to Afghan retail requirements.
**Business Requirement Reference:** Scope Accounting
**Workflow Reference:** Workflow 6
**Description:** Create COA: Cash, Bank, AR, AP, Sales, COGS, Expenses.

##### Technical Design
- **ERPNext Module:** Accounts
- **Doctype Changes:** Account
- **Custom Fields:** None
- **Child Tables:** None
- **Server Scripts:** None
- **Client Scripts:** None
- **Python Files:** None
- **JS Files:** None
- **Print Formats:** None
- **Reports:** None
- **Permissions:** System Manager
- **Role Changes:** None
- **Workflow Changes:** None
- **Notification Changes:** None

##### Impact Analysis
- **Accounting Impact:** Core structure
- **Stock Impact:** None
- **HR Impact:** None
- **API Impact:** None

##### Project Management
- **Dependencies:** 2.1
- **Estimated Complexity:** Medium
- **Estimated Time:** 3 Hours

##### Testing & Quality Assurance
**Acceptance Criteria:**
- COA created

**Manual Test Cases:**
- Review Tree view

**Edge Cases:**

**Regression Test Requirements:**

##### Subtasks
- [ ] Create Accounts

##### GitHub Workflow & Deployment
- **Git Branch Name:** `feat/TASK-8-1`
- **Suggested Commit Message:** `feat: implement Implement Chart of Accounts`
- **Production Deployment Notes:** Standard migration.
- **Rollback Strategy:** Git revert and restore database if necessary.
---

#### Task 8.2: Purchase Invoice Finance Approval Workflow
**Status:** ⬜ Not Started
**Purpose:** Finance Manager must approve PI before payment.
**Business Requirement Reference:** Scope Accounting
**Workflow Reference:** Workflow General Approvals
**Description:** Create Workflow on Purchase Invoice: Pending -> Finance Review -> Finance Manager Approval -> Unpaid/Payable.

##### Technical Design
- **ERPNext Module:** Workflow
- **Doctype Changes:** Purchase Invoice
- **Custom Fields:** None
- **Child Tables:** None
- **Server Scripts:** None
- **Client Scripts:** None
- **Python Files:** None
- **JS Files:** None
- **Print Formats:** None
- **Reports:** None
- **Permissions:** System Manager
- **Role Changes:** None
- **Workflow Changes:** None
- **Notification Changes:** None

##### Impact Analysis
- **Accounting Impact:** Delays GL posting until approved
- **Stock Impact:** None
- **HR Impact:** None
- **API Impact:** None

##### Project Management
- **Dependencies:** 8.1
- **Estimated Complexity:** Medium
- **Estimated Time:** 3 Hours

##### Testing & Quality Assurance
**Acceptance Criteria:**
- PI requires finance approval

**Manual Test Cases:**
- Submit PI

**Edge Cases:**

**Regression Test Requirements:**

##### Subtasks
- [ ] Define Workflow
- [ ] Assign Roles

##### GitHub Workflow & Deployment
- **Git Branch Name:** `feat/TASK-8-2`
- **Suggested Commit Message:** `feat: implement Purchase Invoice Finance Approval Workflow`
- **Production Deployment Notes:** Standard migration.
- **Rollback Strategy:** Git revert and restore database if necessary.
---

#### Task 8.3: Daily Branch Closing with Stock Verification
**Status:** ⬜ Not Started
**Purpose:** Reconcile daily branch POS and Stock.
**Business Requirement Reference:** Scope Accounting
**Workflow Reference:** Workflow 8
**Description:** Customize POS Closing Entry to require a link to a Stock Reconciliation document. Add 'Branch Manager Approval' workflow state.

##### Technical Design
- **ERPNext Module:** Retail
- **Doctype Changes:** POS Closing Entry
- **Custom Fields:** None
- **Child Tables:** None
- **Server Scripts:** None
- **Client Scripts:** None
- **Python Files:** None
- **JS Files:** None
- **Print Formats:** None
- **Reports:** None
- **Permissions:** System Manager
- **Role Changes:** None
- **Workflow Changes:** None
- **Notification Changes:** None

##### Impact Analysis
- **Accounting Impact:** Consolidates POS invoices to Ledger
- **Stock Impact:** None
- **HR Impact:** None
- **API Impact:** None

##### Project Management
- **Dependencies:** 6.1
- **Estimated Complexity:** High
- **Estimated Time:** 6 Hours

##### Testing & Quality Assurance
**Acceptance Criteria:**
- Cannot close without stock recon

**Manual Test Cases:**
- Run POS shift, close shift

**Edge Cases:**
- Stock variance handling

**Regression Test Requirements:**

##### Subtasks
- [ ] Add Stock Recon link field to POS Closing
- [ ] Add Validation Script
- [ ] Add Workflow for Branch Manager Approval

##### GitHub Workflow & Deployment
- **Git Branch Name:** `feat/TASK-8-3`
- **Suggested Commit Message:** `feat: implement Daily Branch Closing with Stock Verification`
- **Production Deployment Notes:** Standard migration.
- **Rollback Strategy:** Git revert and restore database if necessary.
---

# Phase 9: Human Resources
## Module: HRMS
### Feature: Employee Management & Payroll Approval
**Business Process:** Recruitment, Attendance, Payroll with dual approvals.
**Current ERPNext Behavior:** Standard HRMS
**Required Customization:** Install HRMS app and configure payroll workflow.
**Reason:** Workflow 7 & General
**Possible Risks:** Payroll miscalculation
**Testing Strategy:** Payroll testing
**Deployment Strategy:** None

#### Task 9.1: Install and Configure HRMS
**Status:** ⬜ Not Started
**Purpose:** Manage Employees and Attendance.
**Business Requirement Reference:** Scope 8
**Workflow Reference:** Workflow 7
**Description:** Install Frappe HR. Setup Employee master, Attendance, Leave Management.

##### Technical Design
- **ERPNext Module:** HR
- **Doctype Changes:** Employee
- **Custom Fields:** None
- **Child Tables:** None
- **Server Scripts:** None
- **Client Scripts:** None
- **Python Files:** None
- **JS Files:** None
- **Print Formats:** None
- **Reports:** None
- **Permissions:** System Manager
- **Role Changes:** None
- **Workflow Changes:** None
- **Notification Changes:** None

##### Impact Analysis
- **Accounting Impact:** None
- **Stock Impact:** None
- **HR Impact:** Full employee management
- **API Impact:** None

##### Project Management
- **Dependencies:** 1.1
- **Estimated Complexity:** Medium
- **Estimated Time:** 4 Hours

##### Testing & Quality Assurance
**Acceptance Criteria:**
- Employee records created
- Attendance recorded

**Manual Test Cases:**
- Mark attendance

**Edge Cases:**

**Regression Test Requirements:**

##### Subtasks
- [ ] Install HRMS
- [ ] Configure Leave
- [ ] Configure Shifts

##### GitHub Workflow & Deployment
- **Git Branch Name:** `feat/TASK-9-1`
- **Suggested Commit Message:** `feat: implement Install and Configure HRMS`
- **Production Deployment Notes:** Standard migration.
- **Rollback Strategy:** Git revert and restore database if necessary.
---

#### Task 9.2: Payroll Processing & Approval Workflow
**Status:** ⬜ Not Started
**Purpose:** Process salary with HR and Finance approvals.
**Business Requirement Reference:** Scope 8
**Workflow Reference:** Workflow General Approvals
**Description:** Configure Salary Structures. Create Workflow on Salary Slip/Payroll Entry: Pending -> HR Approval -> Finance Approval -> Paid.

##### Technical Design
- **ERPNext Module:** HR
- **Doctype Changes:** Payroll Entry
- **Custom Fields:** None
- **Child Tables:** None
- **Server Scripts:** None
- **Client Scripts:** None
- **Python Files:** None
- **JS Files:** None
- **Print Formats:** None
- **Reports:** None
- **Permissions:** System Manager
- **Role Changes:** None
- **Workflow Changes:** Payroll Approval
- **Notification Changes:** None

##### Impact Analysis
- **Accounting Impact:** Hits payroll expense upon Finance Approval
- **Stock Impact:** None
- **HR Impact:** None
- **API Impact:** None

##### Project Management
- **Dependencies:** 9.1
- **Estimated Complexity:** High
- **Estimated Time:** 5 Hours

##### Testing & Quality Assurance
**Acceptance Criteria:**
- Payroll requires dual approval

**Manual Test Cases:**
- Generate payroll, approve

**Edge Cases:**

**Regression Test Requirements:**

##### Subtasks
- [ ] Setup Salary Components
- [ ] Create Workflow

##### GitHub Workflow & Deployment
- **Git Branch Name:** `feat/TASK-9-2`
- **Suggested Commit Message:** `feat: implement Payroll Processing & Approval Workflow`
- **Production Deployment Notes:** Standard migration.
- **Rollback Strategy:** Git revert and restore database if necessary.
---

# Phase 10: Reports & Dashboards
## Module: Custom Reporting
### Feature: Management Reports
**Business Process:** Custom reports for sales, stock, performance.
**Current ERPNext Behavior:** Standard reports exist.
**Required Customization:** Develop Script Reports.
**Reason:** Workflow 9
**Possible Risks:** Slow queries
**Testing Strategy:** Data testing
**Deployment Strategy:** Python/JS files

#### Task 10.1: Develop Management Reports
**Status:** ⬜ Not Started
**Purpose:** Provide required visibility.
**Business Requirement Reference:** Scope 9
**Workflow Reference:** Workflow 9
**Description:** Create Reports: Branch Sales, Top Selling Items, Slow Moving Items, Inventory Valuation, Gross Profit, Branch Profitability, Supplier Performance, Employee Performance.

##### Technical Design
- **ERPNext Module:** Custom
- **Doctype Changes:** Report
- **Custom Fields:** None
- **Child Tables:** None
- **Server Scripts:** None
- **Client Scripts:** None
- **Python Files:** None
- **JS Files:** None
- **Print Formats:** None
- **Reports:** None
- **Permissions:** System Manager
- **Role Changes:** None
- **Workflow Changes:** None
- **Notification Changes:** None

##### Impact Analysis
- **Accounting Impact:** None
- **Stock Impact:** None
- **HR Impact:** None
- **API Impact:** None

##### Project Management
- **Dependencies:** 8.1
- **Estimated Complexity:** High
- **Estimated Time:** 12 Hours

##### Testing & Quality Assurance
**Acceptance Criteria:**
- All reports exist and accurate

**Manual Test Cases:**
- Run each report

**Edge Cases:**

**Regression Test Requirements:**

##### Subtasks
- [ ] Develop Branch Profitability
- [ ] Develop Employee Performance
- [ ] Develop Top Selling/Slow Moving

##### GitHub Workflow & Deployment
- **Git Branch Name:** `feat/TASK-10-1`
- **Suggested Commit Message:** `feat: implement Develop Management Reports`
- **Production Deployment Notes:** Standard migration.
- **Rollback Strategy:** Git revert and restore database if necessary.
---

# Phase 11: Data Migration & UAT
## Module: Go-Live Prep
### Feature: Data Import & Testing
**Business Process:** Import legacy data and test.
**Current ERPNext Behavior:** Data Import Tool
**Required Customization:** Prepare templates and test scenarios.
**Reason:** Scope 10, 12
**Possible Risks:** Corrupted data
**Testing Strategy:** Balance validation
**Deployment Strategy:** None

#### Task 11.1: Import Master Data & Opening Balances
**Status:** ⬜ Not Started
**Purpose:** Load legacy data.
**Business Requirement Reference:** Scope 10
**Workflow Reference:** None
**Description:** Import Items, Customers, Suppliers, Opening Stock, Opening Financial Balances.

##### Technical Design
- **ERPNext Module:** Data Import
- **Doctype Changes:** Various
- **Custom Fields:** None
- **Child Tables:** None
- **Server Scripts:** None
- **Client Scripts:** None
- **Python Files:** None
- **JS Files:** None
- **Print Formats:** None
- **Reports:** None
- **Permissions:** System Manager
- **Role Changes:** None
- **Workflow Changes:** None
- **Notification Changes:** None

##### Impact Analysis
- **Accounting Impact:** Opening GL balances
- **Stock Impact:** Opening Stock ledger
- **HR Impact:** None
- **API Impact:** None

##### Project Management
- **Dependencies:** 10.1
- **Estimated Complexity:** High
- **Estimated Time:** 16 Hours

##### Testing & Quality Assurance
**Acceptance Criteria:**
- Trial balance matches legacy system

**Manual Test Cases:**
- Check TB

**Edge Cases:**

**Regression Test Requirements:**

##### Subtasks
- [ ] Import Items
- [ ] Import Customers
- [ ] Import Suppliers
- [ ] Import Stock
- [ ] Import Accounts

##### GitHub Workflow & Deployment
- **Git Branch Name:** `feat/TASK-11-1`
- **Suggested Commit Message:** `feat: implement Import Master Data & Opening Balances`
- **Production Deployment Notes:** Standard migration.
- **Rollback Strategy:** Git revert and restore database if necessary.
---

#### Task 11.2: User Acceptance Testing (UAT)
**Status:** ⬜ Not Started
**Purpose:** Validate workflows.
**Business Requirement Reference:** Scope 12
**Workflow Reference:** All Workflows
**Description:** Execute end-to-end testing of Procurement, Main Warehouse Sorting/SKU, Branch Replenishment, POS Sales, Returns, Daily Closing, and Payroll approvals.

##### Technical Design
- **ERPNext Module:** All
- **Doctype Changes:** None
- **Custom Fields:** None
- **Child Tables:** None
- **Server Scripts:** None
- **Client Scripts:** None
- **Python Files:** None
- **JS Files:** None
- **Print Formats:** None
- **Reports:** None
- **Permissions:** System Manager
- **Role Changes:** None
- **Workflow Changes:** None
- **Notification Changes:** None

##### Impact Analysis
- **Accounting Impact:** None
- **Stock Impact:** None
- **HR Impact:** None
- **API Impact:** None

##### Project Management
- **Dependencies:** 11.1
- **Estimated Complexity:** High
- **Estimated Time:** 24 Hours

##### Testing & Quality Assurance
**Acceptance Criteria:**
- All UAT signed off

**Manual Test Cases:**
- Run UAT scenarios with client

**Edge Cases:**

**Regression Test Requirements:**

##### Subtasks
- [ ] Execute Procurement UAT
- [ ] Execute Warehouse UAT
- [ ] Execute POS UAT
- [ ] Execute HR UAT

##### GitHub Workflow & Deployment
- **Git Branch Name:** `feat/TASK-11-2`
- **Suggested Commit Message:** `feat: implement User Acceptance Testing (UAT)`
- **Production Deployment Notes:** Standard migration.
- **Rollback Strategy:** Git revert and restore database if necessary.
---

#### Task 11.3: Production Deployment
**Status:** ⬜ Not Started
**Purpose:** Go-Live.
**Business Requirement Reference:** Scope 12
**Workflow Reference:** None
**Description:** Deploy to production server, train staff, commence support.

##### Technical Design
- **ERPNext Module:** Deployment
- **Doctype Changes:** None
- **Custom Fields:** None
- **Child Tables:** None
- **Server Scripts:** None
- **Client Scripts:** None
- **Python Files:** None
- **JS Files:** None
- **Print Formats:** None
- **Reports:** None
- **Permissions:** System Manager
- **Role Changes:** None
- **Workflow Changes:** None
- **Notification Changes:** None

##### Impact Analysis
- **Accounting Impact:** None
- **Stock Impact:** None
- **HR Impact:** None
- **API Impact:** None

##### Project Management
- **Dependencies:** 11.2
- **Estimated Complexity:** High
- **Estimated Time:** 16 Hours

##### Testing & Quality Assurance
**Acceptance Criteria:**
- System live

**Manual Test Cases:**

**Edge Cases:**

**Regression Test Requirements:**

##### Subtasks
- [ ] Setup Production Server
- [ ] Deploy Custom App
- [ ] Conduct Training

##### GitHub Workflow & Deployment
- **Git Branch Name:** `feat/TASK-11-3`
- **Suggested Commit Message:** `feat: implement Production Deployment`
- **Production Deployment Notes:** Standard migration.
- **Rollback Strategy:** Git revert and restore database if necessary.
---
