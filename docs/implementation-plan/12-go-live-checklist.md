# 12. Go-Live Checklist

This checklist tracks key steps on the day of production deployment.

| Task ID | Task Description | Assigned To | Status | Verification Method |
| :--- | :--- | :--- | :--- | :--- |
| **GL-01** | Freeze staging database and backup config files | Lead Architect | NOT_STARTED | Verify backup archive exists |
| **GL-02** | Configure production server environment variables | SysAdmin | NOT_STARTED | Run `bench config` check |
| **GL-03** | Pull latest `ziad_app` code and run `bench migrate` | Software Lead | NOT_STARTED | Console output verification |
| **GL-04** | Import final Chart of Accounts and Cost Centers | Accountant | NOT_STARTED | Audit COA screen |
| **GL-05** | Verify Item Master and auto-SKU variant settings | Inventory Manager| NOT_STARTED | Validate random variant codes |
| **GL-06** | Import opening stock quantities and valuations | Inventory Manager| NOT_STARTED | Verify Stock Balance report |
| **GL-07** | Import opening accounting balances | Accountant | NOT_STARTED | Review Trial Balance report |
| **GL-08** | Setup POS profiles, cashiers, and connect scanners | Store Managers | NOT_STARTED | Perform a mock $1 scan checkout |
| **GL-09** | Open cashier shifts and confirm initial cash floats | Cashiers | NOT_STARTED | Check POS shift ledger status |
| **GL-10** | Verify automated nightly backup cron job | SysAdmin | NOT_STARTED | Inspect cron logs |
