# 09. Data Migration Plan

A structured roadmap for preparing, validating, and uploading initial master data.

### 1. Migration Split of Responsibilities
*   **Implementation Team:** Prepares blank Excel/CSV import templates for each DocType and configures system settings (Item Groups, Attributes, Chart of Accounts structure).
*   **Client Team:** Cleans, formats, and populates the Excel files with current inventory and account values.
*   **Upload Execution:** The client's team performs the final uploads using ERPNext's native **Data Import** tool.

### 2. Import Sequence & Dependency Mapping
To prevent database validation errors, data must be uploaded in this exact order:

```text
[1. Chart of Accounts] ──> [2. Cost Centers] ──> [3. Branches]
                                                    │
[4. Item Groups] ──> [5. Attributes] ───────────────┼──> [6. Warehouses]
                                                    │
[7. Customers & Suppliers] ─────────────────────────┼──> [8. Items & Variants]
                                                    │
[9. Opening Stock] <────────────────────────────────┴──> [10. Opening Balances]
```

1.  **Chart of Accounts (COA):** Standard structural financial ledgers.
2.  **Cost Centers:** Branch-level financial tagging.
3.  **Branches:** Personnel administrative tagging.
4.  **Item Groups & Attributes:** Pre-requisites for Item creation.
5.  **Warehouses:** Target warehouses for opening inventory.
6.  **Customers & Suppliers:** Required for transactional records.
7.  **Items & Variants:** The product master records (Item templates first, then auto-generated variants).
8.  **Opening Stock (Stock Entry - Material Receipt):** Physical quantity and unit valuation setup.
9.  **Opening Accounting Balances (Journal Entry):** Financial account offsets.
