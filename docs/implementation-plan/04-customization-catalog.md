# 04. Customization Catalog

This catalog details all planned customizations to be developed inside the `ziad_app` codebase.

---

### CUST-01: Auto SKU Generator
*   **Why Needed:** Ensure standardized item variant codes (e.g. `TSH-2026-BLK-L`) across all POS terminals and inventory records.
*   **Impacted DocTypes:** `Item`, `Item Attribute`
*   **Files Changed in `ziad_app`:**
    *   `ziad_app/ziad_app/hooks.py` (Registering event on `Item` DocType)
    *   `ziad_app/ziad_app/ziad_app/item.py` (Python controller logic)
*   **Hooks Added:** `doc_events = { "Item": { "before_insert": "ziad_app.ziad_app.item.generate_sku" } }`
*   **Complexity:** Low
*   **Implementation Order:** 4

---

### CUST-02: Unified Procurement Action (MR -> RFQ)
*   **Why Needed:** Shorten the requisition-to-quote process for purchasing managers.
*   **Impacted DocTypes:** `Material Request`, `Request for Quotation`
*   **Files Changed in `ziad_app`:**
    *   `ziad_app/ziad_app/public/js/material_request.js` (Client-side button)
    *   `ziad_app/ziad_app/ziad_app/api/procurement.py` (Python server API)
*   **Hooks Added:** `doctype_js = { "Material Request": "public/js/material_request.js" }`
*   **Complexity:** Low
*   **Implementation Order:** 6

---

### CUST-03: Dynamic Loyalty Tier Calculator
*   **Why Needed:** Apply the 2.5% and 5% discounts automatically at checkout based on the rolling 6/12-month purchase volume.
*   **Impacted DocTypes:** `Customer`, `Sales Invoice`, `Pricing Rule`
*   **Files Changed in `ziad_app`:**
    *   `ziad_app/ziad_app/hooks.py` (Registering daily scheduler event)
    *   `ziad_app/ziad_app/ziad_app/tasks.py` (Loyalty calculator loop)
*   **Hooks Added:** `scheduler_events = { "daily": [ "ziad_app.ziad_app.tasks.calculate_loyalty_tiers" ] }`
*   **Complexity:** Medium
*   **Implementation Order:** 12

---

### CUST-04: Custom Management Dashboard Reports
*   **Why Needed:** Provide executives with real-time branch profitability metrics and stock turnover.
*   **Impacted DocTypes:** `Sales Invoice`, `Purchase Invoice`, `Stock Ledger Entry`
*   **Files Changed in `ziad_app`:**
    *   `ziad_app/ziad_app/ziad_app/report/branch_profitability/` (Python, JS, HTML report templates)
*   **Hooks Added:** None (Registered via custom report JSON configurations)
*   **Complexity:** Medium
*   **Implementation Order:** 14
