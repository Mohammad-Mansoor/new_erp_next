# Xprinter K200 Thermal Receipt Printer Implementation & Troubleshooting Guide

This document provides a **100% Graphical User Interface (UI-based)** step-by-step guide for setting up, configuring, and troubleshooting the **Xprinter K200 Thermal Receipt Printer** in **ERPNext POS** across **Ubuntu Linux**, **Windows 10/11**, and **macOS**.

---

## 1. Hardware Specifications & Cable Setup

* **Model**: Xprinter K200
* **Paper Width**: 80mm (Printable width: 72mm / 76mm, standard roll size: 80mm x 80mm)
* **Print Speed**: 230 mm/s
* **Interfaces**: Dual Interface (**USB + LAN / Ethernet**)
* **Command Support**: Standard **ESC/POS**
* **Cash Drawer Port**: RJ11 / RJ12 connector (**24V DC / 1A pulse**)

---

## 2. Real-World Challenges & Detailed UI Solutions

During implementation, seven critical real-world challenges were encountered. Use these detailed UI solutions when troubleshooting new POS installations:

### Challenge 1: Auto-Assigned Incorrect Plotter/Laser Driver
* **Symptom**: Printer is detected with model `HP Designjet T920 PostScript` or generic laser.
* **Root Cause**: Operating system auto-assigns a default plotter/laser PostScript driver to unknown USB printers.
* **Impact**: Printer outputs garbage binary code or fails to print.
* **UI Solutions**:
  * **Ubuntu**: Open **Settings $\rightarrow$ Printers $\rightarrow$ 3 Dots $\rightarrow$ Printer Details $\rightarrow$ Driver $\rightarrow$ Select from database $\rightarrow$ Generic $\rightarrow$ ZJ-80** (or `POS-80`).
  * **Windows**: Run **POS Printer Driver Setup v8.xx** wizard GUI and select `POS-80`.
  * **macOS**: **System Settings $\rightarrow$ Printers $\rightarrow$ Select Software $\rightarrow$ Generic ESC/POS Printer**.

---

### Challenge 2: Paper Roll Inserted Upside Down (Paper Feeds Blank)
* **Symptom**: Printer feeds paper and cuts normally, but paper comes out **100% blank with no ink**.
* **Root Cause**: Thermal paper has chemical ink coating on **only one side**.
* **Impact**: Paper is wasted with zero output.
* **UI & Hardware Solution**:
  1. Open top cover and flip the paper roll around so paper unrolls in the opposite direction.
  2. Perform Hardware Self-Test: Turn printer **OFF** $\rightarrow$ Hold **FEED** button $\rightarrow$ Turn **ON** while holding FEED for 2 seconds. A test slip will print in black text.

---

### Challenge 3: Garbled Binary Code Print (Raw Queue vs Raster Driver)
* **Symptom**: Printing from browser produces pages of random garbled text (`%PDF-1.4...` / binary hex dump).
* **Root Cause**: CUPS printer queue configured as `Raw Queue`. Browsers send PDF graphic streams that raw queues cannot interpret.
* **Impact**: Wastes meters of paper printing raw code.
* **UI Solutions**:
  * **Ubuntu**: Open browser at `http://localhost:631` $\rightarrow$ Printers $\rightarrow$ `POS-80` $\rightarrow$ Administration $\rightarrow$ Set Default Options $\rightarrow$ Select **ZJ-80 Raster Driver**.
  * **Windows**: In **Printer Properties $\rightarrow$ Preferences**, select `POS-80 Raster Driver`.

---

### Challenge 4: Landscape Rotation & Invoice Split Across 2 Pages
* **Symptom**: Browser prints receipt sideways in Landscape mode or splits a single invoice across 2 pages.
* **Root Cause**: Driver default page size set to short height (`70x65mm`), causing Chrome to auto-detect Landscape orientation and insert page breaks.
* **Impact**: Receipt is split awkwardly into 2 separate cut sheets.
* **UI Solutions**:
  * **Ubuntu**: Open `http://localhost:631` $\rightarrow$ Set Media Size to **`X70MMY297MM`** (80x297mm). In Chrome `Ctrl + P`: Layout = **Portrait**, Paper = **`X70MMY297MM`**, Margins = **None**.
  * **Windows**: **Printer Properties $\rightarrow$ Preferences $\rightarrow$ Page Setup**: Paper Size = `80 x 297 mm`, Orientation = `Portrait`.
  * **macOS**: **Print Dialog $\rightarrow$ Paper Size $\rightarrow$ Manage Custom Sizes**: Add `80mm x 297mm`, Margins = `0mm`.

---

### Challenge 5: Paper Cutter Clipping Bottom Text & QR Code
* **Symptom**: Physical cutter blade cuts through the last text line or splits the QR code in half.
* **Root Cause**: Physical cutter blade sits ~12mm–15mm above the thermal heating head.
* **Impact**: Important invoice footer details or QR codes are sliced in half.
* **UI Solutions**:
  * **Ubuntu**: In CUPS `http://localhost:631` default options: Set **Blank Space = False** (trim trailing space), **Feed Distance = 2feed9mm** (feed 9mm safety space), and **Cut Media = EndOfPage**.
  * **Windows**: **Printer Properties $\rightarrow$ Device Settings**: Set **Paper Cut = Cut at End of Document** and **Feed Distance = 9mm**.

---

### Challenge 6: Auto-Print Not Triggering on Order Completion (Pop-up Blocker)
* **Symptom**: Cashier completes order in POS, but no print window appears.
* **Root Cause**: Browser blocks automatic pop-up window triggered by ERPNext upon order submission.
* **Impact**: Cashier thinks auto-print is broken.
* **UI Solutions**:
  * **ERPNext Desk**: Open **POS Profile** $\rightarrow$ Check **Print Receipt on Order Complete `[✓]`** $\rightarrow$ Set Print Format to `Modern POS Receipt - POS Invoice`.
  * **Browser UI (Chrome/Chromium)**: Click 3 dots $\rightarrow$ **Settings $\rightarrow$ Privacy and security $\rightarrow$ Site Settings $\rightarrow$ Pop-ups and redirects $\rightarrow$ Add `http://localhost:8000`**.

---

### Challenge 7: Bypassing "Print" Button Prompt (1-Click Silent Kiosk Printing)
* **Symptom**: Cashier must manually click the "Print" button on every single transaction.
* **Root Cause**: Browsers require user confirmation before sending print jobs to hardware.
* **Impact**: Slows down checkout speed during peak hours.
* **UI Solutions**:
  * **Ubuntu**: Right-click Chromium desktop shortcut $\rightarrow$ **Properties** $\rightarrow$ In Command field append `--kiosk-printing`.
  * **Windows**: Right-click Google Chrome desktop shortcut $\rightarrow$ **Properties** $\rightarrow$ In Target field append `--kiosk-printing`.
  * **macOS**: Launch Chrome via shortcut with parameter `--kiosk-printing`.

---

## 3. Step-by-Step UI Setup Guide by Operating System

---

### A. Ubuntu Linux Setup (Complete UI Steps)

#### Step 1: Driver Selection via Ubuntu Settings GUI
1. Open **Settings** $\rightarrow$ Click **Printers**.
2. Click the **kebab menu (3 dots)** next to your printer (`POS-80` or `Xprinter`).
3. Click **Printer Details**.
4. Click on **Driver** (where it shows the driver name).
5. Select **Select from database...**.
6. In the left column (**Manufacturer**), select **Generic** (or **ZJiang**).
7. In the right column (**Driver**), select **ZJ-80** (or **Generic 80mm Receipt Printer**).
8. Click **Select** $\rightarrow$ Click **Apply**.

#### Step 2: Configuring 80mm Paper, Margins & Cutter via CUPS Web GUI
1. Open your web browser and go to: `http://localhost:631`
2. Click on the **Printers** tab at the top $\rightarrow$ Click on **`POS-80`**.
3. Click the **Administration** dropdown menu $\rightarrow$ Select **Set Default Options**.
4. Configure the following UI fields:
   * **Media Size**: Select **`X70MMY297MM`** (80mm width × 297mm height).
   * **Blank Space at page's end**: Select **`False`** (trims blank paper immediately after QR code).
   * **Feed distance**: Select **`2feed9mm`** (feeds 9mm safety space so cutter clears text).
   * **Cut Media**: Select **`EndOfPage`**.
   * **Cutter**: Select **`True`**.
   * **Cash Drawer 1**: Select **`1BeforePrinting`** (if cash drawer is plugged into printer).
5. Click **Set Default Options**.

#### Step 3: Allowing Auto-Print Pop-ups in Chromium GUI
1. Open Chromium $\rightarrow$ Click **3 vertical dots menu** (top right) $\rightarrow$ **Settings**.
2. Left menu: Click **Privacy and security** $\rightarrow$ **Site Settings**.
3. Scroll down under *Permissions* and click **Pop-ups and redirects**.
4. Under **Allowed to send pop-ups and use redirects**, click **Add**.
5. Type your ERPNext site URL: `http://localhost:8000` $\rightarrow$ Click **Add**.

#### Step 4: Enabling Silent Kiosk Printing via Ubuntu Desktop Shortcut
1. Open Ubuntu Files app $\rightarrow$ navigate to your Desktop / Applications folder.
2. Right-click the **Chromium** icon $\rightarrow$ select **Properties**.
3. In the **Command / Exec** box, append `--kiosk-printing` at the end:
   ```text
   chromium --kiosk-printing %U
   ```
4. Click **Close**.

---

### B. Windows 10 / Windows 11 Setup (Complete UI Steps)

#### Step 1: Driver Installation via Setup Wizard GUI
1. Download and double-click `POS Printer Driver Setup v8.xx.exe`.
2. Select OS: **Windows 10** or **Windows 11**.
3. Select Port: **USB** (or **NET / Network IP**).
4. Select Printer Series: **POS-80**.
5. Click **Install Now** $\rightarrow$ Click **Finish**.

#### Step 2: Configuring Paper Size, Cutter & Cash Drawer via Windows Printers GUI
1. Open **Settings** $\rightarrow$ **Bluetooth & Devices** $\rightarrow$ **Printers & Scanners**.
2. Click on **POS-80** $\rightarrow$ Click **Printer Properties**.
3. In the **General** tab $\rightarrow$ Click **Preferences...**:
   * **Page Setup / Paper Size**: Select **`80 x 297 mm`** (or `80 x Continuous`).
   * **Orientation**: Select **`Portrait`**.
4. In the **Device Settings** tab:
   * **Cash Drawer**: Set to **`Pulse Before Printing`** (automatically pops drawer open on sale).
   * **Paper Cut**: Set to **`Cut at End of Document`**.
   * **Feed Distance**: Set to **`9mm`**.
5. Click **Apply** $\rightarrow$ Click **OK**.

#### Step 3: Allowing Pop-ups & Enabling Kiosk Printing in Chrome GUI
1. Open Chrome $\rightarrow$ Settings $\rightarrow$ **Privacy and security** $\rightarrow$ **Site Settings** $\rightarrow$ **Pop-ups and redirects** $\rightarrow$ Add `http://localhost:8000`.
2. Right-click your **Google Chrome** desktop icon $\rightarrow$ Click **Properties**.
3. In the **Target** field, append `--kiosk-printing` at the end of the shortcut target:
   ```text
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --kiosk-printing
   ```
4. Click **Apply** $\rightarrow$ Click **OK**.

---

### C. macOS Setup (macOS Sonoma / Ventura / Sequoia - Complete UI Steps)

#### Step 1: Adding Printer via macOS System Settings GUI
1. Connect printer via USB or LAN.
2. Open **System Settings** $\rightarrow$ **Printers & Scanners**.
3. Click **Add Printer, Scanner, or Fax...** button.
4. Select `POS-80` or `Xprinter`.
5. Under **Use / Driver** dropdown: Click **Select Software...** $\rightarrow$ Choose **Generic ESC/POS Printer** (or **ZJ-80**).
6. Click **Add**.

#### Step 2: Creating Custom 80mm Paper Size via Mac Print GUI
1. Open any web page or PDF and press **`Cmd + P`**.
2. Click on the **Paper Size** dropdown menu $\rightarrow$ Select **Manage Custom Sizes...**.
3. Click the **`+`** button (bottom left) to create a new paper size:
   * **Page Name**: Double click and rename to `Receipt 80mm`.
   * **Width**: Type `80 mm` (3.15 in).
   * **Height**: Type `297 mm` (11.69 in).
   * **Non-Printable Area (Margins)**: Set Top, Bottom, Left, Right to **`0 mm`**.
4. Click **OK**.

#### Step 3: Chrome Pop-ups & Silent Printing on Mac
1. Open Chrome $\rightarrow$ Settings $\rightarrow$ Site Settings $\rightarrow$ Pop-ups $\rightarrow$ Allow `http://localhost:8000`.
2. Launch Chrome with parameter `--kiosk-printing` to enable silent direct printing.

---

## 4. ERPNext POS Profile Setup (UI-Based Step-by-Step)

1. Log into your ERPNext Desk as System Manager.
2. In the search bar, type **POS Profile List** and open your active profile (e.g. `Main Store POS`).
3. Scroll down to **Print Settings**:
   * **Print Format**: Select **`Modern POS Receipt - POS Invoice`**.
   * **Print Receipt on Order Complete**: Check **`[✓]`**.
   * **Letter Head**: Select **`None`**.
4. Click **Save** (top right).

---

## 5. Live Server GitHub Deployment Pipeline

All print formats are stored inside your custom app (`jahan_kodak`) as fixtures (`jahan_kodak/fixtures/print_format.json`).

### To deploy changes to your Live Production Server:
1. **Local Machine (Development)**:
   - Export fixtures: `bench --site development.localhost export-fixtures`
   - Commit & Push to GitHub: `git add .` $\rightarrow$ `git commit -m "docs: add full UI setup and challenges guide"` $\rightarrow$ `git push origin main`
2. **Production / Live Server**:
   - Pull from GitHub: `git pull origin main`
   - Sync Database: `bench --site [live-site-name] migrate`
   - Restart Bench: `bench restart`

All thermal print formats and POS settings will automatically sync to your live server!
