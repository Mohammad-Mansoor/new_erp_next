# Jahan Kodak ERPNext HRMS - Complete Biometric Device Integration Guide

## 1. System Architecture Overview

This document provides an end-to-end, technical and operational guide for integrating multi-branch biometric attendance devices (such as **ZKTeco K40, MB20, MB560-VL**) directly with **ERPNext HRMS** hosted on a **Hostinger VPS**.

### Instant Push Architecture
```
[ Branch 1: Shahr-e-Naw ] ──(Store Internet)──┐
[ Branch 2: Kabul Center ] ──(Store Internet)──┼──> [ Hostinger VPS Nginx (HTTPS) ] ──> [ ERPNext REST API ] ──> [ Employee Checkin ] ──> [ Auto Attendance ]
[ Branch 3: Karteh Naw ]   ──(Store Internet)──┘
```

---

## 2. Phase 1: Biometric Hardware Setup (Store Branches)

### Step-by-step Device Configuration (ZKTeco K40 / MB20 / MB560-VL)

1. **Connect Device to Branch Network:**
   - Plug Ethernet cable (RJ45) into local router OR connect via device Wi-Fi menu.
   - Go to `Menu -> Comm. -> Network -> Ethernet`.
   - Assign static IP address or enable DHCP.

2. **Configure ADMS / Cloud Server Settings:**
   - Go to `Menu -> Comm. -> ADMS` (or `Cloud Server Settings` / `Web Server`).
   - **Enable Domain Name:** `ON` (if using `https://erp.jahankodak.com`) or `OFF` (if using IP).
   - **Server Address:** `erp.jahankodak.com` (or Hostinger VPS Public IP: `185.xxx.xxx.xxx`).
   - **Server Port:** `443` (HTTPS) or `80` (HTTP).
   - **Enable Proxy:** `OFF` (unless store uses proxy).

3. **Enroll Employees & Assign Biometric User IDs:**
   - Go to `Menu -> User Mgt. -> New User`.
   - **User ID:** Assign numeric ID (e.g. `1001` for Employee A, `1002` for Employee B).
   - **Name:** Enter Employee Name.
   - **Enroll:** Register Fingerprints / Face scans / RFID card.

---

### ⚠️ Challenges & Solutions in Phase 1

#### 🚨 Challenge 1.1: ADMS Menu Option is Missing or Greyed Out
* **Root Cause:** Device was flashed with standard standalone firmware without ADMS push protocol.
* **Solution:** Contact supplier before purchasing to ensure **ADMS / Push Firmware** is installed. If already purchased, request the ADMS firmware update `.dat` file from ZKTeco support.

#### 🚨 Challenge 1.2: Branch Internet Drop / Offline Punches
* **Root Cause:** Branch Wi-Fi/Internet disconnects during store hours.
* **Solution:** ZKTeco devices store up to 80,000 logs in internal flash memory. When internet reconnects, the device automatically syncs all offline punches to Hostinger VPS in chronological order.

#### 🚨 Challenge 1.3: Duplicate User IDs Across Different Branches
* **Root Cause:** Branch Manager in Shahr-e-Naw assigns ID `101` to Cashier A, while Branch Manager in Kabul Center assigns ID `101` to Cashier B.
* **Solution:** Implement a strict **Company-wide Biometric ID Naming Convention**:
  - Shahr-e-Naw: `1000 - 1999`
  - Kabul Center: `2000 - 2999`
  - Karteh Naw: `3000 - 3999`
  - Macroyan: `4000 - 4999`

---

## 3. Phase 2: Hostinger VPS Server Setup & Configuration

### Step-by-step Server Configuration

#### 1. Nginx Reverse Proxy Setup
Add location block to your Nginx configuration on Hostinger VPS (`/etc/nginx/conf.d/frappe.conf` or `/etc/nginx/sites-available/development.localhost`):

```nginx
# ADMS Biometric Endpoint Forwarding
location /api/method/hrms.hr.doctype.employee_checkin.employee_checkin.add_log_based_on_employee_field {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    client_max_body_size 10M;
}
```

Reload Nginx:
```bash
sudo systemctl reload nginx
```

#### 2. SSL/TLS Certificate Setup (Certbot)
To allow HTTPS connection from biometric devices:
```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d erp.jahankodak.com
```

---

### ⚠️ Challenges & Solutions in Phase 2

#### 🚨 Challenge 2.1: Old Biometric Firmware Fails SSL Handshake
* **Root Cause:** Older ZKTeco devices do not support modern TLS 1.3 ciphers.
* **Solution:** In Nginx config (`/etc/nginx/nginx.conf`), allow `TLSv1.2`:
  ```nginx
  ssl_protocols TLSv1.2 TLSv1.3;
  ```

#### 🚨 Challenge 2.2: Timezone Mismatch Between Server and Biometric Devices
* **Root Cause:** Hostinger VPS is in UTC, while store device is in Asia/Kabul (+04:30).
* **Solution:** Set Hostinger VPS system timezone to `Asia/Kabul`:
  ```bash
  sudo timedatectl set-timezone Asia/Kabul
  sudo systemctl restart nginx
  ```

---

## 4. Phase 3: ERPNext HRMS UI Configuration

### Step-by-step ERPNext Setup

#### 1. Map Attendance Device ID on Employee Master
1. Navigate to **HR -> Employee -> Select Employee**.
2. Scroll to **Attendance Device ID (Biometric/RF tag ID)** field.
3. Enter exact hardware numeric ID (e.g. `1001`).
4. Click **Save**.

#### 2. Configure Shift Type for Auto Attendance
1. Navigate to **HR -> Shift Type -> Open Shift** (e.g., `JK Retail Morning Shift`).
2. Set **Start Time**: `08:00:00`, **End Time**: `17:00:00`.
3. Check **Enable Auto Attendance**.
4. Set **Determine Check-in and Check-out Based on**: `Alternate entries as IN and OUT` (or `Log Type`).
5. Set **Working Hours Calculation Based On**: `First In and Last Out`.
6. Set **Begin Check-in Before Shift Start Time (Minutes)**: `60`.
7. Set **Allow Check-out After Shift End Time (Minutes)**: `60`.
8. Click **Save**.

---

### ⚠️ Challenges & Solutions in Phase 3

#### 🚨 Challenge 3.1: Punch Marked as "Absent" Despite Check-in Log
* **Root Cause:** Employee checked in at `06:45 AM`, but shift configuration has `Begin Check-in Before Shift Start Time` set to `30 minutes` (07:30 AM). The punch fell outside shift window.
* **Solution:** Increase `Begin Check-in Before Shift Start Time` to `120 minutes` in `Shift Type`.

#### 🚨 Challenge 3.2: Duplicate Logs From Double-Tapping Finger
* **Root Cause:** Staff member scans finger twice within 10 seconds.
* **Solution:** Set **Strict Check-in Buffer (Minutes)** = `5` in `Shift Type`. ERPNext ignores duplicate punches within 5 minutes of previous punch.

---

## 5. Phase 4: Testing, Troubleshooting & Terminal Debugging Commands

### 1. Simulate ADMS Biometric Hit via Terminal (`curl`)
Run this command from any computer to test if Hostinger VPS API is receiving check-ins:

```bash
curl -X POST "https://erp.jahankodak.com/api/method/hrms.hr.doctype.employee_checkin.employee_checkin.add_log_based_on_employee_field" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_field_value": "1001",
    "timestamp": "2026-07-25 08:00:00",
    "device_id": "TEST-DEV-01",
    "log_type": "IN"
  }'
```

**Expected Response:**
```json
{
  "message": {
    "name": "CHECKIN-2026-00001",
    "employee": "HR-EMP-00001",
    "log_type": "IN",
    "time": "2026-07-25 08:00:00"
  }
}
```

### 2. Inspect Live Nginx Traffic Logs on Hostinger VPS
```bash
sudo tail -f /var/log/nginx/access.log | grep "employee_checkin"
```

### 3. Check Scheduler & Auto-Attendance Status via Bench
```bash
bench --site development.localhost doctor
bench --site development.localhost execute hrms.hr.doctype.shift_type.shift_type.process_auto_attendance
```

---

## 6. Phase 5: Production Best Practices & Summary Checklist

| Component | Setting / Command | Purpose |
| :--- | :--- | :--- |
| **Biometric Hardware** | ZKTeco K40 / MB20 with ADMS | Instant hardware push over store internet |
| **Hostinger VPS** | Nginx Reverse Proxy + SSL (TLS 1.2+) | Secure internet endpoint |
| **ERPNext Employee** | `Attendance Device ID` = Biometric User ID | Maps raw punches to staff member |
| **ERPNext Shift Type** | Auto Attendance = Enabled | Automatically generates Daily Attendance |
