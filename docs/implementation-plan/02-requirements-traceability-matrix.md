# 02. Requirements Traceability Matrix (RTM)

This matrix maps each business requirement to the specific ERPNext implementation strategy:
*   **A. Supported natively by ERPNext** (Out-of-the-box configuration)
*   **B. Supported through configuration** (Custom fields, print formats, settings)
*   **C. Supported through workflow customization** (Workflow engine transitions)
*   **D. Supported through custom script** (Client/Server scripts inside `ziad_app`)
*   **E. Requires custom app development** (Creating custom DocTypes/modules in `ziad_app`)
*   **F. Requires external integration** (REST APIs / Webhooks connectivity)

| Req ID | Business Requirement Description | Implementation Type | Target DocType / Module | Status |
| :--- | :--- | :---: | :--- | :--- |
| **REQ-01** | Kabul, Mazar, Herat multi-branch tracking | **B** | Company, Branch, Cost Center | NOT_STARTED |
| **REQ-02** | Central and city warehouse division setup | **B** | Warehouse Tree | NOT_STARTED |
| **REQ-03** | Inter-warehouse inventory transfers | **A** | Stock Entry (Material Transfer) | NOT_STARTED |
| **REQ-04** | POS checkout with barcode/QR scanning guns | **B** | POS Profile, POS Invoice | NOT_STARTED |
| **REQ-05** | Printing QR/Barcode tags for item variants | **B** | Custom Print Format (HTML/CSS) | NOT_STARTED |
| **REQ-06** | Clothing attributes (Size, Color, Brand) | **B** | Item Attribute, Item Template | NOT_STARTED |
| **REQ-07** | Automatic SKU variant naming (e.g. TSH-2026-BLK-L) | **D** | Item (before_insert hook / script) | NOT_STARTED |
| **REQ-08** | Combined Material Request and RFQ flow | **D** | Material Request, RFQ | NOT_STARTED |
| **REQ-09** | Cargo tracking / In-Transit stock flow | **B** | virtual In-Transit Warehouse | NOT_STARTED |
| **REQ-10** | Manufacturing Bill of Materials (BOM) management | **A** | BOM (Manufacturing Module) | NOT_STARTED |
| **REQ-11** | Production Order and raw material consumption | **A** | Work Order, Stock Entry | NOT_STARTED |
| **REQ-12** | Landed Cost allocation (freight, duties) | **A** | Landed Cost Voucher | NOT_STARTED |
| **REQ-13** | Customer Loyalty spend tiers (40k/60k levels) | **D** | Loyalty Program, Server Script | NOT_STARTED |
| **REQ-14** | Employee management, leaves, attendance | **A** | Employee, Attendance (HRMS) | NOT_STARTED |
| **REQ-15** | Payroll and salary slips processing | **A** | Salary Slip (HRMS Payroll) | NOT_STARTED |
| **REQ-16** | Branch and Cost Center accounting ledger | **A** | Chart of Accounts, Journal Entry | NOT_STARTED |
| **REQ-17** | Custom P&L and gross profit margins reports | **B** | Gross Profit Report, SQL Queries | NOT_STARTED |
| **REQ-18** | E-commerce integration (orders/stock sync) | **F** | REST API, Webhooks | NOT_STARTED |
| **REQ-19** | Management dashboard widgets | **B** | Dashboard, Dashboard Chart | NOT_STARTED |
| **REQ-20** | Custom Web Login Page UI Customization | **D** | Custom JS/CSS assets | **COMPLETED** |
