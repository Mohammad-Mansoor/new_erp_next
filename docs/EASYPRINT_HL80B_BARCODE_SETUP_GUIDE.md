# Easy Print ET-HL80B Barcode & QR Label Printer Setup Guide for ERPNext

This document provides a **100% Graphical User Interface (UI-based)** step-by-step guide for setting up, configuring, and troubleshooting the **Easy Print ET-HL80B Thermal Label Printer** for **Item Barcode & QR Sticker Printing** in **ERPNext** across **Ubuntu Linux**, **Windows 10/11**, and **macOS**.

---

## 1. Hardware Specifications & Label Roll Setup

### Printer Specifications (Easy Print ET-HL80B)
* **Model**: Easy Print ET-HL80B
* **Paper Width Range**: 20mm to 80mm (Adjustable physical green paper guide rails inside printer tray)
* **Standard Label Sizes**: `50mm x 35mm` (Default ERPNext sticker size), `40mm x 30mm`, `58mm x 40mm`, `80mm x 50mm`
* **Resolution**: 203 DPI (8 dots/mm)
* **Print Speed**: 180 mm/s
* **Interfaces**: USB + LAN + Bluetooth + WiFi (Quad Interface)
* **Command Support**: TSPL / ESC-POS / ZPL Emulation
* **Power Input**: 24V = 2.5A

---

## 2. Real-World Challenges & Detailed UI Solutions

During barcode label printing setup, several common challenges occur. Use these detailed UI solutions:

### Challenge 1: Label Sensor Miscalibration (Printer Feeds Multiple Blank Stickers)
* **Symptom**: Pressing print outputs 2 to 3 blank label stickers instead of stopping right at the gap between stickers.
* **Root Cause**: The printer's optical gap sensor is not calibrated to the physical height of your label roll stock.
* **Impact**: Text prints across label gaps and wastes sticker rolls.
* **UI & Hardware Solution**:
  1. Turn off printer power switch.
  2. Load label roll so one sticker extends slightly past the front tear bar. Adjust green side rails tightly against the paper edge.
  3. Hold down the **FEED** button $\rightarrow$ Turn power switch **ON**.
  4. Keep holding **FEED** until the printer beeps 2 times and automatically feeds 2 labels to detect the gap. The light will turn green, indicating calibration is complete.

---

### Challenge 2: Page Size Misalignment (Barcode Printed Off-Center or Cut Off)
* **Symptom**: Text or barcode image prints half on the sticker and half on the blank gap or next sticker.
* **Root Cause**: Operating system driver default paper size is set to `80x297mm` or `A4` instead of the exact sticker size (e.g., `50mm x 35mm`).
* **Impact**: Barcode is truncated and unreadable.
* **UI Solutions**:
  * **Ubuntu**: In CUPS `http://localhost:631` $\rightarrow$ Printers $\rightarrow$ `ET-HL80B` $\rightarrow$ Administration $\rightarrow$ Set Default Options $\rightarrow$ Select Media Size **`50mm x 35mm`**.
  * **Windows**: Open **Printer Properties $\rightarrow$ Preferences $\rightarrow$ Page Setup** $\rightarrow$ New Paper Size: Width `50mm`, Height `35mm`.
  * **macOS**: In Print Dialog (`Cmd + P`) $\rightarrow$ Paper Size $\rightarrow$ **Manage Custom Sizes** $\rightarrow$ Add `50mm x 35mm`, Margins `0mm`.

---

### Challenge 3: Fuzzy Barcode / Scanner Unable to Read Printed Barcode
* **Symptom**: The barcode or QR code prints on the label sticker, but handheld barcode scanners fail to scan it.
* **Root Cause**: Low contrast, anti-aliasing blur, or barcode font resolution mismatch at 203 DPI.
* **Impact**: Cashiers cannot scan items at the POS checkout counter.
* **UI & Template Solution**:
  * In ERPNext Print Format CSS, use monochrome high-contrast styling and pixel rendering:
    ```css
    img.barcode, img.qr-code {
        image-rendering: pixelated;
        image-rendering: crisp-edges;
        filter: contrast(200%);
    }
    ```
  * Ensure Jinja template uses clean 1D barcode APIs (e.g. `https://bwipjs-api.metafloor.com/?bcid=code128&text=ITEM-CODE`) or high-resolution QuickChart QR API (`size=200`).

---

### Challenge 4: Printing Multiple Sticker Copies for Inventory Items
* **Symptom**: User needs to print 50 barcode stickers for 50 received stock items, but clicking print only outputs 1 sticker.
* **Root Cause**: Standard browser print dialog defaults to `1 Copy`.
* **UI Solution**:
  * In Browser Print Preview dialog (`Ctrl + P`): Change **Copies** from `1` to `50`.
  * Or use ERPNext **Print Barcode** tool in Stock module (`Stock > Item > Print Barcode`) to specify exact item quantities.

---

## 3. Step-by-Step UI Setup Guide by Operating System

---

### A. Ubuntu Linux Setup (Complete UI Steps)

#### Step 1: Adding Printer & Selecting Driver in Ubuntu Settings GUI
1. Connect Easy Print ET-HL80B via USB cable.
2. Open **Settings** $\rightarrow$ **Printers**.
3. Click **Add Printer...** $\rightarrow$ Select `ET-HL80B` or `Label Printer`.
4. Click **Driver** $\rightarrow$ Select **Select from database...**.
5. Select Manufacturer **Generic** (or **TSPL** / **ZJiang**).
6. Select Driver **Generic Label Printer** (or **ZJ-58 / ZJ-80** / **Label 50x35mm**).
7. Click **Select** $\rightarrow$ Click **Apply**.

#### Step 2: Setting 50mm x 35mm Sticker Size in CUPS Web GUI
1. Open web browser and navigate to: `http://localhost:631`
2. Click **Printers** tab $\rightarrow$ Select `ET-HL80B`.
3. Click **Administration** dropdown $\rightarrow$ Select **Set Default Options**.
4. Configure fields:
   * **Media Size**: Select **`50mm x 35mm`** (or `Custom.50x35mm`).
   * **Media Type**: Select **`Label with Gaps`**.
   * **Print Darkness / Density**: Select **`10`** or **`Dark`** (for sharp black barcode lines).
5. Click **Set Default Options**.

---

### B. Windows 10 / Windows 11 Setup (Complete UI Steps)

#### Step 1: Installing Driver via Windows Setup Wizard GUI
1. Run **Easy Print / Label Printer Driver Setup.exe**.
2. Select OS: **Windows 10 / 11**.
3. Select Interface: **USB** (or **Network / LAN IP**).
4. Select Model: **ET-HL80B** or **80mm Label Printer**.
5. Click **Install**.

#### Step 2: Creating 50mm x 35mm Stock Size in Windows Printer Properties
1. Open **Settings $\rightarrow$ Bluetooth & Devices $\rightarrow$ Printers & Scanners $\rightarrow$ ET-HL80B $\rightarrow$ Printer Properties**.
2. Go to **General** tab $\rightarrow$ Click **Preferences...**.
3. Click **Page Setup** $\rightarrow$ Click **New...** (or **Stock**):
   * **Name**: `Sticker 50x35mm`
   * **Width**: `50.0 mm`
   * **Height**: `35.0 mm`
4. Go to **Device Settings** tab:
   * **Sensor Type**: Select **`Web / Gap`** (Gap between labels).
   * **Post-Print Action**: Select **`Tear Off`**.
5. Click **Apply** $\rightarrow$ Click **OK**.

---

### C. macOS Setup (macOS Sonoma / Ventura / Sequoia - Complete UI Steps)

#### Step 1: Adding Printer via System Settings GUI
1. Open **System Settings $\rightarrow$ Printers & Scanners $\rightarrow$ Add Printer...**.
2. Select `ET-HL80B`.
3. Driver dropdown: Select **Generic PostScript** or **Generic ESC/POS Label Printer**.
4. Click **Add**.

#### Step 2: Creating 50mm x 35mm Custom Size in Mac Print GUI
1. Open any document or item in browser and press **`Cmd + P`**.
2. In **Paper Size** dropdown $\rightarrow$ Click **Manage Custom Sizes...**.
3. Click **`+`** (bottom left):
   * **Name**: `Label 50x35mm`
   * **Width**: `50 mm` (1.97 in)
   * **Height**: `35 mm` (1.38 in)
   * **Margins**: Set Top, Bottom, Left, Right to **`0 mm`**.
4. Click **OK**.

---

## 4. ERPNext Item Barcode & QR Code Print Format Setup

In your ERPNext custom app (`jahan_kodak`), the Item Sticker Print Format **`Item QR Sticker`** is configured for 50mm x 35mm labels:

### Existing HTML & Jinja Template:
```html
<div style="text-align: center; width: 48mm; height: 33mm; padding: 1mm; font-family: Arial, sans-serif; background-color: #ffffff; color: #000000; box-sizing: border-box;">
    <!-- Company Name / Item Name -->
    <div style="font-size: 11px; font-weight: bold; margin-bottom: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
        {{ doc.item_name }}
    </div>
    
    <!-- 1D Barcode Image -->
    <img src="https://bwipjs-api.metafloor.com/?bcid=code128&text={{ doc.item_code or doc.name }}&scale=2&height=10" 
         style="width: 42mm; height: 14mm; margin: 0 auto; display: block; image-rendering: pixelated;" 
         alt="Barcode" />
         
    <!-- Item Code & Price -->
    <div style="font-size: 10px; font-weight: bold; margin-top: 2px; display: flex; justify-content: space-between; padding: 0 2mm;">
        <span>{{ doc.name }}</span>
        <span>{{ doc.get_formatted('standard_rate') if doc.standard_rate else '' }}</span>
    </div>
</div>

<style>
    @page { 
        size: 50mm 35mm; 
        margin: 0; 
    }
    html, body { 
        margin: 0; 
        padding: 0; 
        background-color: #ffffff !important;
        color: #000000 !important;
    }
</style>
```

### How to Assign Item Barcode Print Format in ERPNext:
1. Open ERPNext Desk $\rightarrow$ Go to **Item List** (`Stock > Item`).
2. Open any Item (e.g., product record).
3. Click **Print** icon (top right) or press `Ctrl + P`.
4. Select Print Format: **`Item QR Sticker`**.
5. In browser print dialog:
   * **Destination**: Select `ET-HL80B`
   * **Paper Size**: Select `50mm x 35mm`
   * **Margins**: Set to **None**
6. Click **Print**.

---

## 5. Live Server GitHub Deployment Pipeline

The `Item QR Sticker` print format is saved inside `jahan_kodak/fixtures/print_format.json`.

To push and deploy to production:
1. **Local Machine**:
   ```bash
   bench --site development.localhost export-fixtures
   cd apps/jahan_kodak
   git add .
   git commit -m "docs: add Easy Print ET-HL80B barcode label printer guide"
   git push origin main
   ```
2. **Live Production Server**:
   ```bash
   cd ~/frappe-bench/apps/jahan_kodak
   git pull origin main
   cd ~/frappe-bench
   bench --site [live-site-name] migrate
   bench restart
   ```
All barcode sticker print formats will automatically update across your live ERPNext system!
