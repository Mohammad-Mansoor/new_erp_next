# 14. Technical Decision Log (TDL)

This log records major technical and architectural decisions, their trade-offs, and justifications.

---

### DEC-01: ERPNext v15 Adoption
*   **Date:** 2026-06-07
*   **Context:** Selection of stable version for retail and manufacturing.
*   **Decision:** Implement ERPNext v15.
*   **Justification:** Version 15 offers a highly stabilized POS module, enhanced manufacturing costing, and separate HRMS application maintenance, making it more modular and robust.
*   **Status:** APPROVED

---

### DEC-02: "Wrap and Extend" Customization Strategy
*   **Date:** 2026-06-07
*   **Context:** Deciding how to apply custom CSS/JS and logic overrides.
*   **Decision:** Maintain all customizations in a separate application (`ziad_app`). Core codebases must remain completely clean.
*   **Justification:** Protects the system from upgrading conflicts, simplifies Git branch merges, and isolates custom features.
*   **Status:** APPROVED

---

### DEC-03: Keyboard Emulation for Barcode/QR Scanning
*   **Date:** 2026-06-10
*   **Context:** Deciding on integration drivers for retail checkout scanners.
*   **Decision:** Use standard barcode/QR guns configured to operate as keyboard emulation devices.
*   **Justification:** Standardizes integration; scanners type characters directly into standard browser text inputs, removing the need for operating-system-level custom drivers.
*   **Status:** APPROVED
