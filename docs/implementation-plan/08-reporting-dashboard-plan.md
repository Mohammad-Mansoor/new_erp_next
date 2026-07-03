# 08. Reporting & Dashboard Plan

This document plans the structure of operational reports and custom executive dashboards.

### 1. Executive Management Dashboard
Designed for real-time visualization of multi-branch revenue and inventory health:

*   **Widget 1: Daily Sales by Branch**
    *   *Type:* Grouped Bar Chart
    *   *Source:* `POS Invoice` filtered by Posting Date (Today) and grouped by Warehouse/Branch.
*   **Widget 2: Gross Profit Margin (Branch and Item Group)**
    *   *Type:* Donut Chart
    *   *Source:* `Gross Profit` query, plotting cost of goods sold (COGS) against sales values.
*   **Widget 3: Inventory Shortage Alert**
    *   *Type:* List Widget (Warning)
    *   *Source:* Displays items currently below their defined Reorder Level or Safety Stock limit.

### 2. Custom Reports (to be created in `ziad_app`)

#### Branch Profitability Report
*   *Type:* Script Report (Python + JS)
*   *Parameters:* Fiscal Year, Cost Center, Branch.
*   *Logic:* Extracts Sales Revenue (from Sales Invoices linked to the branch cost center), subtracts Cost of Goods Sold (COGS), issues/deducts branch expenses (salaries, food, rent, utilities logged against branch cost centers), and displays net margin per branch.

#### Stock Turnover Report
*   *Type:* Query Report (SQL)
*   *Logic:* Calculates the ratio of COGS to average inventory value over 3, 6, and 12-month periods to identify slow-moving and fast-selling items across branches.
