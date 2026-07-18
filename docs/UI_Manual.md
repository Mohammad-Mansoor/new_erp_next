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

### 4. Setting up Users, Defaults, & Data Security (Version 15)
If staff asks: *"How do we set up a Cashier or Branch Manager, set their defaults, and ensure they only see their own branch's data?"*
**The Answer:**
In Version 15, we use **Roles**, **POS Profiles**, and **User Permissions**.
1. **Assign Roles:** From the User Profile, assign roles like **Branch Manager** or **Sales User**. A user can hold multiple roles (e.g., acting as both Manager and Cashier).
2. **Set Defaults & Security:** In ERPNext v15, User Defaults and Data Security are combined. Go to **User Permissions** (search in the global bar) and click **Add User Permission**.
3. Create permission records for the user's assigned Warehouse, Cost Center, and Cash Account.
4. **CRITICAL:** Check both the **"Is Default"** and **"Apply to all Document Types"** checkboxes for each record.
5. **The Result:** When the user logs in, the system will auto-fill their specific Branch details on every new document. Furthermore, it invisibly filters every database query. It is mathematically impossible for them to view another branch's data.
6. **For POS (Cashiers):** Create a **POS Profile** for the branch, link it to the branch's Warehouse, Cost Center, and Cash Account, and add the user to the "Applicable for Users" table (making sure to check the "Default" checkbox in that table).

### 5. Workflow System Notifications
If staff asks: *"Why aren't we getting email notifications for approvals?"*
**The Answer:**
* We rely on **System Notifications** to prevent email spam. 
* When a document requires a Branch Manager's approval, the system generates a "To Do" record specifically for users with the Branch Manager role who have permission for that branch.
* This "To Do" instantly triggers the **Bell Icon** notification in the top right of the ERPNext screen. Clicking the bell takes the manager straight to the document they need to approve.

---

### Phase 5: Manufacturing & Production (Version 15 Guide)

Manufacturing in ERPNext requires a strict sequence. You cannot produce a finished item without telling the system *where* it is made, *what* tasks are performed, *what* materials are used, and *how* to execute the order.

#### The Master DocType Flow (Zero to Finished Good)
If you are starting from an absolutely empty system, you **must** create records in this exact chronological order. You cannot skip a step, or the system will block you:
1. **Workstation:** Define the physical machine or room and its hourly cost.
2. **Operation:** Define the physical task (e.g., Sewing) and link it to the Workstation.
3. **Item (Raw Material):** Create the physical ingredients. Must have `Maintain Stock` and `Is Purchase Item` checked.
4. **Item (Finished Good):** Create the final product. Must have `Maintain Stock` and `Is Sales Item` checked.
5. **Stock Entry (Material Receipt):** You must physically have raw materials in your warehouse, or production will fail due to negative stock.
6. **Bill of Materials (BOM):** Build the recipe linking the Raw Materials (Step 3), the Finished Good (Step 4), and the Operations (Step 2) together.
7. **Work Order:** The official command to the factory to produce a specific quantity using the BOM.
8. **Job Card:** The worker's timesheet. They must submit this to prove they completed the operation and to lock in the labor cost.
9. **Stock Entry (Manufacture):** The final step (clicking 'Finish' on the Work Order) that deletes the raw materials and magically creates the finished goods in the target warehouse.

### 1. Prerequisites: Operations and Workstations
Before building a recipe, the system needs to know about your factory floor.
* **Workstation:** The physical location or machine (e.g., `Sewing Room`, `Cutting Table`). You assign "Hour Rates" (e.g., $10/hour) to workstations so the system can calculate labor costs.
  * **How to create:** Search **Workstation List** -> **Add Workstation**. Fill in the Name and Hourly Costs.
* **Operation:** The actual action performed by human or machine (e.g., `Sewing`, `Cutting`). 
  * **How to create:** Search **Operation List** -> **Add Operation**. Fill in the Name and optionally link a Default Workstation.

### 2. Creating Raw Materials
Before you can manufacture a shirt, you need raw materials (like fabric and thread) in your system.
**How to do it from the UI:**
1. Go to **Item List** and click **Add Item**.
2. **Item Name:** Define your raw material (e.g., `Cotton Fabric - Blue`).
3. **Item Group:** Set to **Raw Materials**.
4. **Default Unit of Measure (UOM):** Set correctly (e.g., `Meter` or `Kg`).
5. **Checkboxes (CRITICAL):** 
   * Uncheck **Is Sales Item** (You do not sell raw fabric to customers).
   * Check **Maintain Stock** (To track inventory levels).
   * Check **Is Purchase Item** (To allow buying from suppliers).
6. **Save** the Item.

### 3. Creating the Recipe: Bill of Materials (BOM)
**What is a BOM?** A Bill of Materials is the strict "blueprint" or "recipe" for creating a finished garment. It links the Raw Materials and Operations together. 

#### Understanding Every BOM Field & Tab
When you create a BOM, you will see multiple tabs. Here is exactly what each tab and field means, and how to use them:

**1. Production Item Tab (The Basic Blueprint)**
*   **Item:** Select the finished garment you are trying to produce (e.g., `PRO-2026...`).
*   **Company:** Select your main company.
*   **Item UOM:** The Unit of Measure (e.g., `Nos`, `Set`).
*   **Quantity:** *Extremely Important.* This is how many units this specific recipe makes. Usually, you set this to `1` so the recipe is for exactly 1 shirt. 
*   **Is Active:** Check this so the factory can actually use this BOM.
*   **Is Default:** If you have multiple recipes for the same shirt (e.g., a fast recipe and a cheap recipe), check this on your primary recipe so the system auto-selects it.
*   **Allow Alternative Item:** Check this if a specific raw material runs out of stock, and you want to allow the factory manager to legally swap it with a different permitted material without throwing an error.
*   **Set rate of sub-assembly item based on BOM:** If this BOM uses another manufactured part as a raw material (e.g., you manufacture the collar separately), check this so the system calculates the collar's live cost rather than its static valuation rate.
*   **Items Table (Raw Materials):** This is your ingredient list. Add a row for every raw material needed to make the `Quantity` specified above. The system will automatically fetch the real-time **Rate (AFN)** and calculate the **Amount**.

**2. Operations Tab (The Labor & Machinery)**
*   **With Operations:** **CRITICAL.** If you leave this unchecked, the system assumes humans work for free. You must check this to track labor and electricity costs!
*   **Transfer Material Against:** Usually set to `Work Order`. This tells the system how you plan to move the raw materials from the main warehouse to the factory floor.
*   **Operations Table:** Add a row for every physical step (e.g., `Cutting`, `Sewing`). 
    *   **Workstation:** Where the step happens.
    *   **Operation Time:** How many minutes it takes to do this step for the `Quantity` specified. If you change the quantity later, this time multiplies.
    *   **Fixed Time:** Time that *never* multiplies (e.g., it takes 30 minutes to clean and set up the sewing machine, regardless of whether you are making 1 shirt or 500 shirts).
    *   **Operating Cost:** The system automatically multiplies the Operation Time by the Workstation's Hourly Rate to calculate the exact AFN labor cost.

**3. Scrap & Process Loss Tab (The Waste)**
*   **Scrap Items Table:** If cutting the fabric produces leftover scraps that still have *some* value (e.g., you sell the scraps for cheap), you list the scrap item here. The system will automatically move the scrap to a Scrap Warehouse during production so you don't lose its financial value.
*   **% Process Loss:** This is for invisible waste (e.g., thread snapping, liquid evaporating). If you expect 5% of the fabric to just be completely ruined and thrown in the garbage, you put `5` here. The system will automatically consume 5% *more* raw materials to ensure you still successfully produce the final shirt, absorbing the cost of the waste.

**4. Costing Tab (The Financial Summary)**
*   *This tab is 100% automatic and read-only.*
*   **Operating Cost:** The total sum of all labor and machine costs from Tab 2.
*   **Raw Material Cost:** The total sum of all physical ingredients from Tab 1.
*   **Total Cost (AFN):** The exact financial value that your finished shirt will have when it enters the warehouse. 

**5. More Info Tab**
*   **Quality Inspection Required:** Check this if you want to legally block the factory workers from clicking "Finish" on the Work Order until a Quality Manager has inspected the shirts and signed off on them.
*   **Item Name / Description:** Standard description fields.

**How to Save:** Once you have filled out these tabs, click **Save** and then **Submit**. The recipe is now locked and active.

### 4. The Production Cycle: Work Orders
**What is a Work Order?** While a BOM is just a recipe, a Work Order is the actual command to the factory floor to start cooking. 
**Scenario:** The main office orders the factory to produce 500 units of the blue Nike shirt.
**How to do it from the UI:**
1. Type **Work Order** in the global search and click **Add Work Order**.
2. **Item to Manufacture:** Select your finished shirt (`PRO-2026-MEN-NIK-M-BLU`).
3. **BOM No:** The system automatically fetches the default BOM recipe you just created.
4. **Qty to Manufacture:** Enter `500`. (The system instantly multiplies the BOM recipe by 500).
5. **Warehouse Settings (CRITICAL for v15):**
   * **Source Warehouse:** Where the raw materials are currently stored (e.g., `Raw Material Warehouse`).
   * **WIP Warehouse (Work In Progress):** A virtual warehouse representing the factory floor. When production starts, raw materials sit here.
   * **Target Warehouse:** Where the finished 500 shirts will be stored (e.g., `Finished Goods Warehouse`).
6. **Save** and **Submit** the Work Order. It is now in "Not Started" status.

### 5. Executing the Work Order (Start & Finish)
Now the factory floor actually does the work.
1. **Start Production:** The factory manager opens the Work Order and clicks the blue **Start** button. 
   * *What happens:* It asks how many units you are starting. If you say 500, it creates a **Stock Entry (Material Transfer for Manufacture)**. This moves 750 meters of fabric from the Source Warehouse into the WIP Warehouse.
2. **Finish Production:** Once the physical sewing is done, the manager clicks the **Finish** button.
   * *What happens:* It creates a **Stock Entry (Manufacture)**. The system permanently consumes/deletes the 750 meters of fabric from the WIP Warehouse, and magically generates 500 Finished Shirts in the Target Warehouse. 
   * *The Accounting:* The finished shirts automatically inherit the financial value of the raw materials PLUS the labor costs calculated from the Operations table!

---

## Phase 6: POS & Sales (Version 15 Guide)

To run a retail branch properly, you need to set up how you accept money, restrict cashiers to their specific branch, and enforce a strict approval process for customer refunds so cashiers cannot steal money.

### 1. Setting Up Modes of Payment
Before opening the shop, we must define exactly how customers can pay.
1. Type **Mode of Payment** in the global search bar and click **Add Mode of Payment**.
2. Create three separate records: `Cash`, `Bank Card`, and `Mobile Money`.
3. **CRITICAL:** For each one, scroll down to the **Accounts** table. Add a row, select your **Company**, and select the exact **Default Account** in your chart of accounts (e.g., link "Cash" to your physical branch Cash Drawer account, link "Bank Card" to your main Bank account).
4. Save each one.

### 2. Configuring the POS Profile (Detailed Guide)
The POS Profile is the absolute core of retail operations. It legally binds a cashier to a specific warehouse, limits what they can edit, and sets the accounting defaults so they don't have to think about finance.
1. Type **POS Profile** in the search bar and click **Add POS Profile**.

**Details Tab:**
*   **Name:** The name of the register (e.g., `Karte Naw Branch POS`).
*   **Company:** Select `Jahan Kodak`.
*   **Customer:** Select a generic customer (e.g., `Walk-In Customer`). This stops cashiers from being forced to type a name for every single person buying a shirt.
*   **Warehouse:** Select the specific branch's warehouse (e.g., `Karteh Naw - JK`). This ensures stock is deducted from this exact store.
*   **Applicable for Users:** Add the user account(s) of the Cashiers who will operate this register. If a user is not listed here, they cannot open the POS.
*   **Payment Methods:** Add the modes you just created (`Cash`, `Bank Card`). Check the **Default** box for `Cash`.

**Configuration Tab (Security Settings):**
*   **Hide Unavailable Items:** **CHECK THIS.** This prevents cashiers from trying to sell a shirt that has 0 stock in the warehouse.
*   **Validate Stock on Save:** **CHECK THIS.** This ensures the system strictly blocks negative inventory.
*   **Print Receipt on Order Complete:** **CHECK THIS.** Automatically prints the receipt so the cashier doesn't have to manually click print.
*   **Allow User to Edit Rate / Edit Discount:** **UNCHECK THESE.** Unless you want your cashiers to have the power to manually change prices or give random discounts, keep these unchecked for security!

**Filters Tab:**
*   **Item Groups:** If you only want this POS to sell `Products` (Finished Goods) and hide `Raw Materials`, add `Products` here. 

**Print Settings Tab:**
*   **Print Format:** Select your POS receipt layout so the printer knows what to print.

**Accounting Tab (Financial Automation):**
*   **Price List:** Select `Standard Selling`.
*   **Currency:** Select `AFN`.
*   **Write Off Account & Cost Center:** If a customer's total is 999 AFN but they pay 1000 AFN and say "keep the change", the 1 AFN difference is routed to this account.
*   **Write Off Limit:** Type `1.00` to allow the system to auto-absorb up to 1 AFN of rounding differences.
*   **Account for Change Amount:** Select your physical Cash account (this tells the system where "change" given back to the customer comes from).
*   **Income Account:** Select your `Sales` account.
*   **Expense Account:** Select your `Cost of Goods Sold` account.
*   **Cost Center:** Select the branch's specific Cost Center so the branch P&L report is accurate.

Click **Save**. Your POS register is now fully secure and financially automated!

### 3. Creating the Return Approval Workflow
When a customer brings back a defective shirt, the cashier must process a return. To prevent cashiers from processing fake returns and pocketing the cash, we will enforce a strict Workflow where only a Branch Manager can approve the refund.
1. Type **Workflow** in the search bar and click **Add Workflow**.
2. **Workflow Name:** `POS Return Approval`.
3. **Document Type:** Select `POS Invoice`.
4. **Is Active:** Check the box.
5. **Conditions (CRITICAL):** In the condition box, type exactly this: `doc.is_return == 1`. *(This is magical: it tells ERPNext that normal sales do NOT need approval, ONLY refunds!)*
6. **Workflow States:** Create these rows:
   * `Draft` (Doc Status: 0)
   * `Pending Refund Approval` (Doc Status: 0)
   * `Approved` (Doc Status: 1 - Submitted)
   * `Rejected` (Doc Status: 2 - Cancelled)
7. **Transition Rules:** Create these rows:
   * State: `Draft` -> Action: `Request Refund` -> Next State: `Pending Refund Approval` -> Allowed Role: `Sales User` (or Cashier)
   * State: `Pending Refund Approval` -> Action: `Approve` -> Next State: `Approved` -> Allowed Role: `Branch Manager`
   * State: `Pending Refund Approval` -> Action: `Reject` -> Next State: `Rejected` -> Allowed Role: `Branch Manager`
8. Save.

### 4. Setting the Selling Price
Before the cashier can sell the shirt, the system needs to know how much to charge the customer. In ERPNext, prices are kept separate from the physical item.
1. Type **Item Price** in the search bar and click **Add Item Price**.
2. **Item Code:** Select your item (e.g., `Red T-Shirt`).
3. **Price List:** Select `Standard Selling`. *(This is critical: it must exactly match the Price List you selected in the Accounting tab of your POS Profile!)*
4. **Rate:** Enter the final selling price (e.g., `1000`).
5. Save. The POS will now automatically fetch this exact price when the item is scanned!

### 5. Opening the Shift & Selling (Testing the POS)
Now it is 8:00 AM, and the cashier arrives for work.
1. Type **Point of Sale** in the search bar.
2. The system will ask you to open a **POS Shift**. Select the `Kabul Center Register 1` profile you created, enter the opening float (e.g., how much change is in the physical drawer right now), and click open.
3. You are now in the POS UI! Click on a `Red T-Shirt` to add it to the cart.
4. Click **Pay**. You will see Cash, Bank Card, and Mobile Money. 
5. *Cool Feature:* You can split payments! If the shirt is 1000 AFN, type 500 in Cash, and 500 in Bank Card.
6. Click **Complete Order**. The stock is instantly deducted from the warehouse!

### 6. Advanced POS Scenarios (Returns & Exchanges)
In the real world, retail gets messy. Here is exactly how to handle common, complex situations securely:

**Scenario A: The Full Return**
*Customer brings back the shirt and wants a full refund.*
1. In the POS UI, click the menu (or Recent Orders) and find the past sale.
2. Click **Return**. The system loads the entire invoice as negative (e.g., `-1` shirt, `-200` AFN).
3. The cashier clicks **Pay** and saves the return. Because of the Workflow we built, it cannot be submitted yet.
4. The cashier clicks **Request Refund**.
5. The **Branch Manager** verifies the shirt is physically there, clicks **Approve**, and only then does the cashier hand back 200 AFN.

**Scenario B: The Partial Return**
*Customer bought 10 shirts, but only 1 of them has a rip. They want to return just 1.*
1. In the POS UI, find the past sale of 10 shirts and click **Return**.
2. The system will load all 10 shirts as negative (`-10` shirts).
3. **The Fix:** The cashier must manually click on the shirt inside the POS cart and change the quantity from `-10` to `-1`. 
4. The system instantly recalculates the refund amount to only cover that 1 single shirt. The cashier requests approval and processes the return normally!

**Scenario C: The Exchange / Price Negotiation**
*Customer bought a shirt for 200 AFN, but finds a small stain. They say: "I am going to return this... UNLESS you let me keep it for 150 AFN."*
1. First, find the order and click **Return**. The cart shows `-1` shirt, `-200` AFN.
2. Now, *without leaving that exact same cart screen*, search the item list and click the shirt to add it as a brand new sale. The cart now has two rows: the return (`-1`) and the new sale (`+1`).
3. **The Security Check:** Because we explicitly unchecked "Allow User to Edit Rate" and "Allow User to Edit Discount" in the POS Profile earlier, the cashier is mathematically blocked from just typing "150". 
4. **The Fix:** The cashier must call the Branch Manager. The manager uses their secure code to apply a 50 AFN Discount to the new `+1` shirt. This absolute security ensures cashiers cannot fake "stains" just to sell cheap shirts to their friends!
5. The cart total will automatically merge everything (`-200` old + `150` new) and show a final Grand Total of `-50` AFN. You hand the customer 50 AFN, and everyone is happy!
