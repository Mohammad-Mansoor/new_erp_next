# 10. Testing Strategy

This strategy outlines the verification phases to guarantee the reliability of customized business workflows.

### 1. Testing Phases
1.  **Unit Testing (CI):** Automating python unit tests in `ziad_app` (testing Variant Auto-SKU naming formulas and loyalty group transitions).
2.  **Sandbox Integration Testing:** Deploying configurations on a dedicated staging database instance.
3.  **User Acceptance Testing (UAT):** Guided client validation of core scenarios.

### 2. Standard UAT Test Scripts

#### UAT-01: End-to-End Retail Sales Scenario
*   **Pre-requisites:** Scanning gun connected, cash drawer shift opened, items have variant SKU barcodes.
*   **Test Steps:**
    1.  Open POS screen. Scan the barcode/QR code label for item variant `TSH-2026-BLK-M`.
    2.  Verify the variant is added to the cart with correct pricing.
    3.  Select a Loyalty Customer, verify if any automatic Pricing Rule discounts apply.
    4.  Submit payment, print receipt, close shift.
*   **Acceptance Criteria:**
    *   Item is successfully added to cart via keyboard emulation.
    *   POS invoice prints with correct details.
    *   Stock levels decrease in target Warehouse.
    *   Accounting entries post to the branch Cost Center.

#### UAT-02: Cargo Receipt and Transfer
*   **Test Steps:**
    1.  Create Purchase Receipt to "In-Transit Cargo" warehouse. Verify inventory is added there.
    2.  Verify Accounts Payable is correctly affected.
    3.  Create Stock Entry (Material Transfer) to move 50 items from "In-Transit Cargo" to "Kabul Central" warehouse.
*   **Acceptance Criteria:**
    *   In-Transit Warehouse balance decreases by 50.
    *   Kabul Central Warehouse increases by 50.
    *   No accounting ledger impact is posted (simple stock relocation).
