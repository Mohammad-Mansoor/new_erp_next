# ERPNext UI Manual: Jahan Kodak

This document provides step-by-step instructions on how to manually create or manage the automated components through the ERPNext User Interface. It also highlights critical business rules to keep in mind to maintain system integrity.

---

## Phase 2: Core Configuration & Master Data

### 1. Creating a New Branch
**How to do it from the UI:**
1. Type **Branch** into the global search bar at the top of the screen and select **Branch List**.
2. Click the blue **Add Branch** button (top right).
3. Enter the name of the new branch (e.g., `Mazar Center`).
4. Click **Save**.

**Important things to keep in mind:**
- A Branch in ERPNext is just a label used for grouping. Creating a branch here does **not** automatically create a Cost Center, Warehouse, or POS Profile for it. You must always complete the subsequent steps below to fully integrate a new branch into your financial and operational workflows.

### 2. Creating a Cost Center for a Branch
**How to do it from the UI:**
1. Type **Chart of Cost Centers** in the global search bar.
2. In the tree view, locate your root cost center folder (e.g., `Jahan Kodak - JK`).
3. Click on the root folder and select **Add Child**.
4. In the popup, fill out the following fields:
   - **Cost Center Name:** Name it clearly using your convention (e.g., `Mazar Center - JK`).
   - **Company:** `Jahan Kodak`
   - **Is Group:** Make sure this is **unchecked**. (Only check this if you are creating a parent folder to hold other sub-cost centers).
5. Click **Create New**.

**Important things to keep in mind:**
- **Financial Integrity:** Never delete a cost center that already has financial transactions (like sales or expenses) tied to it. If a branch permanently closes, you should rename it or disable it, but deleting it will break past Profit & Loss (P&L) reports.
- **Tree Structure:** Always ensure the new Cost Center is placed strictly under the correct parent folder (`Jahan Kodak - JK`) so your central office management dashboards can accurately sum up the company-wide totals.

---

## Phase 3: Inventory & Warehouses

### 1. Creating a New Warehouse
**How to do it from the UI:**
1. Type **Warehouse Tree** into the global search bar and select it.
2. Locate the parent folder where the warehouse should live (e.g., `All Warehouses - JK`).
3. Click on the parent folder and select **Add Child**.
4. In the popup, fill out:
   - **Warehouse Name:** (e.g., `Herat Center`)
   - **Is Group:** Unchecked (unless this warehouse will contain sub-warehouses).
5. Click **Create New**.

**Important things to keep in mind:**
- **Inventory valuation:** If you delete or rename a warehouse, ERPNext handles it safely, but if the warehouse currently holds stock, you **cannot** delete it. You must first transfer the stock out to a zero balance.
- Always ensure branches are nested under the correct root warehouse so reports run accurately.

### 2. Creating New Item Attributes (Size, Color, Brand)
**How to do it from the UI:**
1. Search for **Item Attribute** and go to the List View.
2. Click **Add Item Attribute**.
3. Provide the Attribute Name (e.g., `Fabric`).
4. In the **Item Attribute Values** table, add rows for each value (e.g., `Cotton`, `Silk`) and provide an `Abbr` (Abbreviation) for each (e.g., `COT`, `SIL`).
5. Click **Save**.

**Important things to keep in mind:**
- The **Abbr (Abbreviation)** column is absolutely critical. Our custom Server Script relies on this exact abbreviation to automatically generate your Item SKUs (e.g., `TSH-2026-COT`). If you leave it blank, the script will just take the first 3 letters.

### 3. Creating Items and Auto-Generating SKUs
**How to do it from the UI:**
1. Create an Item Template (Search **Item List** -> **Add Item**). 
2. Check the **Has Variants** checkbox.
3. In the **Variant Attributes** table, add rows for all the attributes you want (e.g., `Persone category`, `Gender`, `Brand`, `Size`, `Colour`).
4. **CRITICAL:** Leave the **Attribute Value** column completely blank! Do not try to click or type into it.
5. Click **Save** in the top right to save the master blueprint.
6. Once saved, click the **Create** button (top right) -> **Variant** (or use the Multiple Variants tool).
7. Select your specific values (e.g., Gender: `Men`, Brand: `Nike`) and save. 
8. The custom background script will instantly kick in and automatically rename the Variant's Item Code and Name by dynamically stringing together all abbreviations! (e.g., `PRO-2026-MEN-NIK...`).

**Important things to keep in mind:**
- **Dynamic Naming:** The script is 100% dynamic. It will read whatever attributes you added to the template in the exact order you added them. It pulls the 3-letter abbreviation from the `Item Attribute Value` table. 
- If the SKU generates incorrectly (e.g., it says `XXX`), it means you forgot to set an Abbreviation in the Item Attribute Value settings, so it didn't know what letters to use!

---

## Phase 4: Procurement & Custom Fields

### 1. Modifying the Flexible Workflows
Unlike rigid hardcoded workflows, we have built the **"JK Material Request Flow"** using ERPNext's native Workflow engine. It intelligently routes both Transfers and Purchases based on conditions.
**How to manage it from the UI:**
1. Type **Workflow List** in the global search bar.
2. Click on **JK Material Request Flow**.
3. Under the **Transitions** table, you can freely change exactly who is allowed to approve what by modifying the `Allowed` Role column.
4. If you need a new approval stage (e.g., *CEO Approval*), simply add a new State and define the Transition! 

### 2. Modifying Custom Fields (Cargo Tracking)
We have added `Cargo Company`, `Cargo Tracking Number`, and `Expected Arrival Date` to the Purchase Order. Because this is flexible, you can add more at any time without a developer.
**How to manage it from the UI:**
1. Open any **Purchase Order** and click the **three dots** in the top right.
2. Select **Customize**.
3. Scroll down to the fields table. You will see our custom Cargo fields there.
4. You can freely rename them, change their position, or add new rows (e.g., `Driver Phone Number`) just by clicking **Add Row**.
5. Click **Update** to save the changes instantly across the entire system.

### 3. Business Scenario: Branch vs Central Purchasing
If staff asks: *"How do we order things if branches aren't allowed to buy from suppliers?"*
**The Answer:** 
* Branches **never** use the "Purchase" purpose on a Material Request. 
* A branch user creates a Material Request and sets the purpose to **Material Transfer** (requesting goods from the Central Warehouse). 
* The custom workflow automatically skips Procurement and sends this directly to the Central Warehouse team for approval and dispatch (via a Stock Entry).
* If the Central Warehouse is out of stock, *they* (the main office) create a Material Request for **Purchase**, which then goes through the strict Branch Manager and Procurement approval flow.

### 4. Setting up a Branch Manager & Data Security
If staff asks: *"How do we assign a manager to a branch, and ensure they only see their own branch's data?"*
**The Answer:**
We use Roles and User Permissions.
1. Assign the user the **Branch Manager** role from their User Profile.
2. Go to **User Permissions** (search in the global bar).
3. Create a new User Permission linking that user to their specific branch (e.g., `Kabul Center`).
4. **CRITICAL:** Ensure the **"Apply to all Document Types"** checkbox is checked.
5. **The Result:** The system will now invisibly filter every database query for that user. They will only see Material Requests, Sales, and Inventory for `Kabul Center`. It is mathematically impossible for them to view another branch's data.

### 5. Workflow System Notifications
If staff asks: *"Why aren't we getting email notifications for approvals?"*
**The Answer:**
* We rely on **System Notifications** to prevent email spam. 
* When a document requires a Branch Manager's approval, the system generates a "To Do" record specifically for users with the Branch Manager role who have permission for that branch.
* This "To Do" instantly triggers the **Bell Icon** notification in the top right of the ERPNext screen. Clicking the bell takes the manager straight to the document they need to approve.

---

## Phase 5: Manufacturing & Production

### 1. Creating Raw Materials
Before you can manufacture a shirt, you need raw materials (like fabric and thread) in your system.
**How to do it from the UI:**
1. Go to **Item List** and click **Add Item**.
2. Create your raw material (e.g., `Cotton Fabric - Blue`).
3. **CRITICAL:** Set the `Item Group` to **Raw Materials - JK**.
4. Uncheck `Is Sales Item` (because you don't sell raw fabric to customers).
5. Check `Maintain Stock` and `Is Purchase Item`.
6. Save the Item.

### 2. Creating the Recipe (Bill of Materials - BOM)
A Bill of Materials (BOM) is the strict recipe for creating one unit of a finished garment.
**How to do it from the UI:**
1. Type **BOM** in the global search bar and click **Add BOM**.
2. **Item:** Select the finished Variant you want to produce (e.g., `PRO-2026-MEN-NIK-M-BLU`).
3. **Quantity:** Set to 1 (this recipe makes 1 unit).
4. **Operations Table:** Add the steps required. We have pre-configured `Cutting`, `Sewing`, `Quality Check`, and `Packaging`. Specify the Workstation (e.g., `Sewing Floor`) and the operating time (in minutes). The system will automatically calculate the labor cost based on the workstation's hourly rate!
5. **Materials Table:** Add the raw materials needed for this 1 unit (e.g., 2 meters of `Cotton Fabric - Blue`). 
6. **Save** and **Submit** the BOM.

### 3. The Production Cycle (Work Orders)
When the factory floor is ready to produce 500 shirts, they use a Work Order.
**Business Scenario:** The main office wants 500 units of the blue Nike shirt.
1. Type **Work Order** in the global search and click **Add Work Order**.
2. Select the Item to manufacture (`PRO-2026-MEN-NIK-M-BLU`).
3. ERPNext automatically pulls the BOM you just created.
4. Set the **Qty to Manufacture** to 500.
5. Select the **Source Warehouse** (where the raw materials are stored, usually Central Warehouse) and the **Target Warehouse** (where the finished 500 shirts will go).
6. **Save** and **Submit**.
7. **Start Production:** The factory manager clicks **Start**, which deducts the raw fabric (500 x 2 = 1,000 meters) from the warehouse. When they finish, they click **Finish**, and 500 finished shirts magically appear in the target warehouse, with their precise financial value perfectly calculated!
