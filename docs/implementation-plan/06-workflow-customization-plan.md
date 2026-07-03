# 06. Workflow Customization Plan

This document establishes document states, roles, and transition permissions for critical business processes.

### 1. Procurement Custom Workflow
Unifies the requisition and approvals pipeline:

```text
[Draft] -> (Submitter) -> [Pending Manager Approval] -> (Manager) -> [Approved for Quote] -> (Buyer) -> [RFQ Issued]
```

*   **States:**
    1.  `Draft` (Edit permitted by Submitter)
    2.  `Pending Manager Approval` (Read-only for Submitter, Edit/Approve permitted by Purchase Manager)
    3.  `Approved for Quote` (Read-only, accessible by Purchase User)
    4.  `RFQ Issued` (Read-only, finalized state)
*   **Transition Rules:**
    *   Submitter submits document $ightarrow$ changes state to `Pending Manager Approval`.
    *   Manager approves $ightarrow$ changes state to `Approved for Quote` (Triggers visual "Create RFQ" button).
    *   Buyer links RFQ and submits $ightarrow$ changes state to `RFQ Issued`.

### 2. Cargo Transit Workflow
Tracks container shipment progress:

```text
[Dispatched] -> (Carrier Manager) -> [In Ocean Transit] -> (Customs Agent) -> [Customs Clearance] -> (Receiver) -> [Received at Central]
```

*   **States:**
    1.  `Dispatched` (Assigned when Supplier releases goods)
    2.  `In Ocean Transit` (Updated when shipping container is loaded)
    3.  `Customs Clearance` (Updated during local port processing)
    4.  `Received at Central` (Finalized, triggers transfer to physical inventory)
