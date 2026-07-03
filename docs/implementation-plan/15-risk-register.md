# 15. Risk Register

This register identifies risks that could impact project schedule or system quality:

| Risk ID | Risk Description | Probability | Impact | Mitigation Strategy | Owner |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **RSK-01** | Client delays cleaning and compiling master excel sheets | Medium | High | Provide empty templates in Month 1, check progress weekly, and run test uploads with partial data in Month 3. | Project Manager |
| **RSK-02** | Complex 6/12 month loyalty calculation affects database performance | Low | Medium| Optimize SQL query indexes, run calculation as a nightly background job during off-hours, and cache results on the Customer record. | Lead Architect |
| **RSK-03** | E-commerce API sync latency during peak sales hours | Medium | Medium| Implement queue-based background tasks (using Frappe's native redis queue worker) to update stock asynchronously rather than synchronously. | Software Lead |
| **RSK-04** | Cashiers struggle to adapt to the new digital POS interface | High | Medium| Deploy UAT sandbox terminal early for practice scans, and conduct structured cashier-specific training sessions. | Store Manager |
| **RSK-05** | Production server downtime or data corruption | Low | High | Configure automated off-site backups every 24 hours, and perform monthly recovery restoration audits. | SysAdmin |
