# Branch Sync Configuration Guide

This document explains exactly how to configure the `Branch Sync Config` on both the **Cloud Server** (master) and the **Local Servers** (branches) so they can communicate securely and reliably.

---

## Accessing the Configuration
1. Log into your ERPNext Desk.
2. In the global search bar (Awesome Bar) at the top, search for: **Branch Sync Config**
3. Click the result to open the configuration form.

---

## Configuration Fields Explained

### 1. Branch ID
* **What it is**: The unique identifier for a physical branch (e.g., `BR01`, `KABUL_MAIN`).
* **Cloud Server**: Set this to the ID of the specific branch you are configuring the credentials for.
* **Local Server**: Set this to its own identity (e.g., `BR01`). This MUST perfectly match what is expected by the Cloud.

### 2. API Key
* **What it is**: A public identifier for the branch.
* **Usage**: You can set this to anything descriptive like `BR01-KEY`. It is primarily for reference and future API extensions.

### 3. API Secret
* **What it is**: The most critical security setting. This is a **Shared Symmetric Key** used for HMAC-SHA256 cryptographic signatures.
* **Usage**: You **do not** generate this from the standard ERPNext user system. You must manually type a strong, random password (e.g., `a8b9c4x7!9kL2pQ`). 
* **Rule**: You must copy and paste the **exact same secret** into the Cloud Server's config and the Local Server's config. If they differ by even one character, all sync traffic will be rejected as "Tampered / Invalid Signature".

### 4. Cloud URL
* **What it is**: The internet-accessible web address of your Master Cloud Server.
* **Cloud Server**: You can leave this blank or set it to its own domain.
* **Local Server**: **MANDATORY**. You must set this to the full HTTPS URL of the Cloud (e.g., `https://cloud.jahankodak.com`). The Local Server uses this address to actively push POS Invoices and pull Stock Deltas. Do not add trailing slashes (e.g., avoid `...com/`).

### 5. Is Cloud Server (Checkbox)
* **What it is**: The behavioral toggle that tells the `jk_sync` codebase who it is.
* **Cloud Server**: **MUST BE CHECKED.** When checked, the server knows it is the master. It will accept incoming data, evaluate global dependencies, and generate Stock Deltas for the branches. It will NOT attempt to push data out.
* **Local Server**: **MUST BE UNCHECKED.** When unchecked, the server knows it is a physical branch. It will actively run background jobs every minute to poll the Cloud URL, pull down master data updates, and push up its POS transactions.

---

## Summary Checklist for a New Branch Setup

**On the Cloud Server:**
- [ ] `Branch ID`: BR01
- [ ] `API Secret`: (Strong Password)
- [ ] `Is Cloud Server`: **CHECKED**

**On the Local Server (BR01):**
- [ ] `Branch ID`: BR01
- [ ] `API Secret`: (Exact Same Strong Password)
- [ ] `Cloud URL`: https://cloud.jahankodak.com
- [ ] `Is Cloud Server`: **UNCHECKED**
