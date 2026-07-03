# 01. Project Overview
## Clothing Retail ERP Implementation (Ziad App)

### 1. Introduction & Executive Summary
This document defines the implementation strategy and architectural blueprint for migrating and centralizing the client's retail, manufacturing, stock, accounting, and HR workflows onto **ERPNext v15** and the **Frappe Framework**. The project is scoped for a **5-month implementation timeline**, followed by **4 months of support** (up to 2 months client-led sandbox testing and validation, and 2 months post-go-live production server maintenance and minor bug fixing).

### 2. System Architecture Vision
We adhere to a **"Wrap and Extend"** architecture to guarantee long-term system stability, easy upgradability, and maintainability:
*   **Frappe Framework (v15):** Handles core ORM, database schema management, user authentication, security, REST API, and web-assets serving.
*   **ERPNext (v15):** Delivers pre-built modules for Stock, Procurement, Point of Sale, Manufacturing, and Accounting.
*   **HRMS App:** Extends ERPNext with advanced employee profiling, leave management, attendance tracking, and local payroll processing.
*   **Ziad App (`ziad_app`):** The custom application containing all customized schemas (DocTypes), client-side JS controllers, server-side Python event hooks, custom print layouts, and dashboard reports. **Core codebases of Frappe, ERPNext, and HRMS remain completely unmodified.**

```mermaid
graph TD
    subgraph Core Apps
        frappe[Frappe Framework v15]
        erpnext[ERPNext v15]
        hrms[HRMS App]
    end
    subgraph Custom Layer
        ziad_app[Ziad Custom App: ziad_app]
    end
    subgraph Client Touchpoints
        pos[POS Terminal Web Browsers]
        admin[Management Desk]
        ecommerce[E-Commerce Website]
    end

    ziad_app -->|Hooks & Overrides| Core Apps
    pos -->|Rest API / Web UI| ziad_app
    admin -->|Web Desk UI| ziad_app
    ecommerce -->|REST API Integration| ziad_app
```

### 3. Current Codebase Audited State
A complete scan of the active codebase has been performed to map existing assets:
*   **Existing Customizations:** Custom Login Screen UI styles and animations are implemented.
*   **CSS Asset:** `/apps/ziad_app/ziad_app/public/css/ziad_app.css` (Glassmorphism layout, background gradients, and form alignments).
*   **JS Asset:** `/apps/ziad_app/ziad_app/public/js/ziad_app.js` (DOM restructuring and background orb animations).
*   **Hooks Configuration:** Assets are registered under `web_include_css` and `web_include_js` inside `/apps/ziad_app/ziad_app/hooks.py` with cache-busting version query parameters (`?v=1.0.3`).
*   **DocTypes, Reports, & Scripts:** Currently, no custom DocTypes, reports, or background server event scripts are registered. The custom app is clean and ready to host custom structures.
