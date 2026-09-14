# Cloud Server Deployment Guide: Step-by-Step

This guide provides exactly what you need to deploy the **Cloud Server** (Master Node) from an absolute zero state (a fresh Ubuntu OS) to a live production state. 
You can log into your fresh server via SSH and copy/paste these commands one by one.

## 1. System Update & Dependencies
We assume a fresh installation of **Ubuntu 24.04 LTS** (which includes Python 3.12).
*Explanation: Updates the package manager and installs standard tools we will need later.*
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl wget software-properties-common cron xvfb libfontconfig wkhtmltopdf libmysqlclient-dev
```

## 2. Create the Frappe User
*Explanation: Frappe/ERPNext strictly refuses to run as the root user for security reasons. We create a user named `frappe` and give it sudo (admin) rights.*
```bash
sudo adduser frappe
sudo usermod -aG sudo frappe
su - frappe
```
> [!IMPORTANT]  
> After running `su - frappe`, your terminal prompt will change. You are now acting as the `frappe` user. All the following commands must be run as this user!

## 3. Install Python, Node.js, Redis, and Nginx
*Explanation: ERPNext is built on Python and uses Node.js for building web assets. Redis is used for caching and background tasks, while Nginx will act as the web server.*
```bash
# Install Python 3.12 virtual environment tools
sudo apt install -y python3-dev python3-pip python3-venv python3-virtualenv

# Download and run the Node.js setup script (using v20.x for Frappe 15 compatibility)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -

# Install Node.js
sudo apt install -y nodejs

# Install yarn globally (required by Frappe to compile assets)
sudo npm install -g yarn

# Install Redis server, Nginx web server, and Supervisor (process manager)
sudo apt install -y redis-server nginx supervisor
```

## 4. Install & Configure MariaDB
*Explanation: ERPNext relies on MariaDB. We must install it and configure the exact character sets so Frappe doesn't throw encoding errors.*
```bash
# Install MariaDB
sudo apt install -y mariadb-server mariadb-client
```

Now we configure it. Copy and paste this exact block of text to safely append the settings into the configuration file:
```bash
sudo bash -c 'cat << EOF >> /etc/mysql/mariadb.conf.d/50-server.cnf

[mysqld]
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

[mysql]
default-character-set = utf8mb4
EOF'
```

*Explanation: Restart the database service so it reads the new settings.*
```bash
sudo systemctl restart mariadb
```

*Explanation: Secure the database. You MUST answer the prompts. Set a strong root password, remove anonymous users, and disallow root login remotely.*
```bash
sudo mysql_secure_installation
```

## 5. Install Frappe Bench
*Explanation: `bench` is the command-line tool you use to manage ERPNext instances.*
```bash
sudo pip3 install frappe-bench --break-system-packages
```
*(Note: Ubuntu 24.04 requires `--break-system-packages` when installing pip packages globally).*

## 6. Initialize the Bench Environment
*Explanation: We initialize a new environment folder called `frappe-bench` locking it to `version-15`.*
```bash
cd ~
bench init frappe-bench --frappe-branch version-15
cd frappe-bench
```

## 7. Download Applications
*Explanation: We download ERPNext, HRMS, and your two custom GitHub repositories into the bench.*
```bash
# Get Standard Apps
bench get-app payments
bench get-app erpnext --branch version-15
bench get-app hrms --branch version-15

# Get Custom Apps
bench get-app jahan_kodak https://github.com/Mohammad-Mansoor/new_erp_next.git
bench get-app jk_sync https://github.com/Mohammad-Mansoor/new_erp_next_jk_sync.git
```

## 8. Create the Cloud Site
*Explanation: We create the actual website database. It will prompt you for the MariaDB root password you set earlier, and ask you to create the Administrator password for ERPNext.*
```bash
export SITE_NAME="cloud.jahankodak.com"

bench new-site $SITE_NAME
```

## 9. Install Apps on the Cloud Site
*Explanation: We instruct the site to install the database tables for all these apps.*
```bash
bench --site $SITE_NAME install-app payments
bench --site $SITE_NAME install-app erpnext
bench --site $SITE_NAME install-app hrms
bench --site $SITE_NAME install-app jahan_kodak
bench --site $SITE_NAME install-app jk_sync
```

## 10. Configure Production Server
*Explanation: This command automatically generates the Nginx (web) and Supervisor (background worker) configuration files so the site stays alive automatically, even after server reboots.*
```bash
sudo bench setup production frappe
```

*Explanation: This tells Nginx that this site is the default one to load when someone visits the server IP.*
```bash
bench use $SITE_NAME
```

---

## 11. Final Setup
Your Cloud Server is now live.

1. Open your web browser and go to your server's IP or Domain.
2. Login as `Administrator` using the password you set in step 8.
3. Finish the ERPNext setup wizard.
4. Search for **Branch Sync Config**, check the **Is Cloud Server** box, and generate your API Secrets for the branches to connect to.
