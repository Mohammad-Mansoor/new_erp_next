# 03. Gap Analysis

This document details identified operational gaps between standard ERPNext v15 functionality and the client's requirements, and explains the architecture to bridge them.

### 1. Gap: Automatic Attribute-Based SKU Variant Generation (REQ-07)
*   **Standard ERPNext behavior:** Item variants generate codes based on either a global naming series, a template code prefix plus attribute abbreviations, or manually defined codes. Standard configurations can sometimes fail to handle complex custom year or collection structures (e.g., extracting year attributes dynamically).
*   **Resolution Strategy:** Use a Server Script on the `Item` variant before-insert event. The script reads the parent Item Template and selected attributes, generates the standardized code format (e.g., `[Prefix]-[Year]-[ColorCode]-[SizeCode]`), checks for uniqueness, and writes it to the variant's `item_code` field.

### 2. Gap: Unified Material Request & Request for Quotation (REQ-08)
*   **Standard ERPNext behavior:** Material Request and Request for Quotation are treated as two separate documents that require separate navigation and manual creation steps.
*   **Resolution Strategy:** Inject a custom **Client Script** via `ziad_app` into the `Material Request` DocType. The script adds a custom button "Create RFQ" in the header of approved Material Requests. Clicking this automatically makes an API call to a whitelisted python method that creates the RFQ, copies all items, and opens the new RFQ in the UI.

### 3. Gap: In-Transit Cargo Pipeline (REQ-09)
*   **Standard ERPNext behavior:** Purchase Receipt assumes direct receipt of goods into the final target warehouses. Simple purchase transitions do not trace multi-week cargo transit, sea freight containers, or port clearance status.
*   **Resolution Strategy:** Set up virtual warehouses under the parent warehouse tree named **"In-Transit Cargo [City]"**. Goods shipped by suppliers are checked into "In-Transit Cargo" using a Purchase Receipt (signaling ownership and accounts payable impact). Once the shipping containers arrive and clear customs, a **Stock Entry (Material Transfer)** is created to distribute items from "In-Transit Cargo" to the physical branch warehouses.

### 4. Gap: Rolling 6/12 Month Loyalty Tier Adjustments (REQ-13)
*   **Standard ERPNext behavior:** ERPNext's Loyalty Program calculates loyalty points based on transaction values. It does not natively support a rolling 6/12 month historical sales audit that automatically shifts customers into discount groups (e.g., 2.5% and 5%) when total spending hits 40k or 60k.
*   **Resolution Strategy:** Create a nightly scheduled **Server Script** (running via scheduler event `daily` in `hooks.py`). The script queries the sum of completed `Sales Invoice` documents for each customer over the past 6 and 12 months. If the sum exceeds 40,000 or 60,000, it automatically updates the customer's loyalty category or Customer Group, triggering active **Pricing Rules** (2.5% and 5% discounts) linked to that customer segment.
