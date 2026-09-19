# Event Streaming Configuration Guide

This document explains exactly how to configure ERPNext's native **Event Streaming** to synchronize static/structural configurations from the Master Cloud Server to your Local Branch Servers.

## Why Use Event Streaming?
Our custom `jk_sync` application is designed strictly for high-speed, offline-durable transactional data (like Sales, Inventory, Customers, and Item Prices). 

However, ERPNext requires foundational settings (like Users, Warehouses, and POS Profiles) to be perfectly identical across all servers. Instead of typing these manually on every local server, we use ERPNext's native Event Streaming to automatically copy them over.

---

## 1. Cloud Server Setup (The Producer)

The Cloud Server acts as the source of truth. You will generate an API Key here so the local branches are authorized to pull data.

### Step 1: Generate an API Key
1. Log into your **Cloud Server** ERPNext Desk as Administrator.
2. In the global search bar, type **User** and open the User list.
3. Open the `Administrator` user profile (or create a dedicated user named `sync_admin`).
4. Scroll down to the **API Access** section.
5. Click **Generate Keys**.
6. A popup will appear containing the **API Key** and the **API Secret**. 
   > [!IMPORTANT]
   > Copy the **API Secret** into a notepad immediately! ERPNext will only ever show this to you once for security reasons.

*That is all you have to do on the Cloud Server!*

---

## 2. Local Server Setup (The Consumer)

The Local Server will use the keys generated above to subscribe to changes on the Cloud Server.

### Step 1: Create the Event Producer Connection
1. Log into your **Local Server (Branch)** ERPNext Desk as Administrator.
2. In the global search bar, type and open: **Event Producer List**.
3. Click **Add Event Producer**.
4. Fill in the connection details:
   - **Producer URL**: `https://cloud.jahankodak.com` *(Replace with your actual Cloud URL)*
   - **Producer Node**: You can leave this blank.
   - **API Key**: *(Paste the API Key you copied from the Cloud Server)*
   - **API Secret**: *(Paste the API Secret you copied from the Cloud Server)*

### Step 2: Configure the Subscribed DocTypes
Scroll down to the **Event Configuration** table. This is where you tell the Local Server exactly which tables it is allowed to copy from the Cloud.

Click **Add Row** for every single item in this list. 
For every row you add, you **MUST** check the box for `Use Same Name`. This guarantees the internal IDs match perfectly.

#### Safe DocTypes to Add (Add ALL of these):
1. `User` *(Syncs cashier accounts and passwords)*
2. `Role` *(Syncs permissions)*
3. `Warehouse` *(Syncs branch warehouse definitions)*
4. `POS Profile` *(Syncs the configuration of your POS screens)*
5. `Cost Center` *(Syncs financial accounting centers)*
6. `Account` *(Syncs your Chart of Accounts)*
7. `Item Group` *(Syncs product categories)*
8. `Customer Group` *(Syncs customer categories)*
9. `Mode of Payment` *(Syncs Cash/Credit configurations)*
10. `POS Payment Method` *(Syncs the mapping of payments)*
11. `Company` *(Syncs company configurations so linked Accounts and Warehouses do not break!)*

> [!CAUTION]
> **NEVER add the following DocTypes to this list:** `Item`, `Item Price`, `Customer`, `Customer Merge Log`, `Stock Entry`, `Stock Ledger Entry`, `POS Invoice`, `POS Closing Entry`, or `GL Entry`. Adding these will cause catastrophic collisions with the `jk_sync` app and corrupt your local inventory math.

### Step 3: Activate the Stream
1. Scroll back to the top of the **Event Producer** page.
2. Check the box that says **Is Active**.
3. Click **Save**.

If the connection is successful, the status indicator at the top will change to **Approved**.

---

## 3. How it Works in Production

From now on, whenever you need to hire a new cashier, change an account, or create a new Warehouse:
1. You make the change **once** on the Cloud Server.
2. Every few minutes, a background job on the Local Server asks the Cloud Server, *"Did anything change in my subscribed DocTypes?"*
3. The Cloud Server replies with the changes, and the Local Server updates itself silently. 

You get perfect structural synchronization with zero manual effort!
