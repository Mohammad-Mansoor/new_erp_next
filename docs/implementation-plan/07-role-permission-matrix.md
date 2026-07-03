# 07. Role Permission Matrix

This matrix details access controls across key DocTypes for the various implementation roles:

| Role | DocType | Read | Write | Create | Delete | Submit | Cancel | Amend |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **System Manager** | *All* | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| **POS Cashier** | POS Invoice | Yes | Yes | Yes | No | Yes | No | No |
| **POS Cashier** | Item | Yes | No | No | No | No | No | No |
| **Warehouse Keeper**| Stock Entry | Yes | Yes | Yes | No | Yes | Yes | Yes |
| **Warehouse Keeper**| Warehouse | Yes | No | No | No | No | No | No |
| **Accountant** | Journal Entry | Yes | Yes | Yes | No | Yes | Yes | Yes |
| **Accountant** | Purchase Invoice| Yes | Yes | Yes | No | Yes | Yes | Yes |
| **Accountant** | Sales Invoice | Yes | Yes | Yes | No | Yes | Yes | Yes |
| **Purchase User** | Material Request| Yes | Yes | Yes | No | Yes | Yes | Yes |
| **Purchase User** | RFQ | Yes | Yes | Yes | No | Yes | Yes | Yes |
| **Purchase Manager**| Purchase Order | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| **Production User** | Work Order | Yes | Yes | Yes | No | Yes | No | No |
| **Production User** | BOM | Yes | No | No | No | No | No | No |
| **HR Manager** | Employee | Yes | Yes | Yes | Yes | No | No | No |
| **HR Manager** | Salary Slip | Yes | Yes | Yes | No | Yes | Yes | Yes |
| **Branch Manager** | Reports | Yes | No | No | No | No | No | No |
