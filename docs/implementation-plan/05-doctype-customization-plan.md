# 05. DocType Customization Plan

This document details modifications to native DocTypes (via custom fields/property setters) and custom DocTypes to be created in `ziad_app`.

### 1. Native DocType Customizations

#### Item
*   **Add Custom Field:** `abbreviation` (Data field in Item Attribute Value child table to store BLK, L, etc.)
*   **Add Custom Field:** `collection_year` (Select field in Item Template to define Collection Year, e.g. 2026)

#### Purchase Receipt
*   **Add Custom Field:** `is_cargo_transit` (Check field, default = 0. Shows whether goods are still in sea/air cargo)
*   **Add Custom Field:** `cargo_tracking_no` (Data field to store container or tracking reference)

#### Customer
*   **Add Custom Field:** `rolling_sales_6m` (Currency field, Read-Only, updated by daily background scheduler)
*   **Add Custom Field:** `rolling_sales_12m` (Currency field, Read-Only, updated by daily background scheduler)

---

### 2. Custom DocTypes (to be created)

#### Cargo Shipping Voyage (`Cargo Shipping Voyage`)
*   **Module:** Stock
*   **Why Needed:** Track imports, container shipping statuses, customs clearances, and link them to respective Purchase Receipts.
*   **Fields:**
    *   `title` (Data, Auto-name)
    *   `carrier` (Link to Supplier)
    *   `shipment_type` (Select: Sea, Air, Land)
    *   `departure_date` (Date)
    *   `estimated_arrival` (Date)
    *   `customs_clearance_status` (Select: Pending, Cleared, Disputed)
    *   `purchase_receipts` (Table: linked to incoming goods)
