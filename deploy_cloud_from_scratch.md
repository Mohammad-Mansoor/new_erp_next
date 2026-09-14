# Cloud Server Deployment Guide (From Zero to Live)

This guide provides step-by-step instructions to set up a brand new Ubuntu server from scratch, install all prerequisites (Node, Python, MariaDB, Redis), install Frappe, ERPNext, HRMS, and your custom apps (`jahan_kodak` and `jk_sync`), and configure it for production on the **Cloud Server**.

---

## 1. Server Prerequisites & OS Setup
We assume you are running a fresh installation of **Ubuntu 22.04 LTS**.

Log in to your server as `root` (or a user with sudo privileges) and update the system:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl wget software-properties-common cron
```

## 2. Create the Frappe User
Frappe cannot be run as `root`. We must create a dedicated user.
```bash
sudo adduser frappe
sudo usermod -aG sudo frappe
su - frappe
```

*Note: Run all subsequent commands as the `frappe` user.*

## 3. Install Python, Node.js, Redis, and Nginx
ERPNext requires Python, Node.js (for asset compilation), Redis (for caching and queues), and Nginx (for web serving).

```bash
# Install Python and dependencies
sudo apt install -y python3-dev python3-pip python3-venv python3-virtualenv
sudo apt install -y xvfb libfontconfig wkhtmltopdf libmysqlclient-dev

# Install Node.js (v18) and Yarn
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
sudo npm install -g yarn

# Install Redis, Nginx, and Supervisor
sudo apt install -y redis-server nginx supervisor
```

## 4. Install & Configure MariaDB
ERPNext uses MariaDB as its relational database.

```bash
sudo apt install -y mariadb-server mariadb-client
```

Configure MariaDB for Frappe by editing the configuration file:
```bash
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
```
Add the following block under `[mysqld]`:
```ini
[mysqld]
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

[mysql]
default-character-set = utf8mb4
```

Restart MariaDB and run the secure installation:
```bash
sudo systemctl restart mariadb
sudo mysql_secure_installation
```
*(Follow the prompts to set a root password, remove anonymous users, and disallow root login remotely)*

## 5. Install Frappe Bench CLI
Bench is the command-line utility used to manage Frappe environments.

```bash
sudo pip3 install frappe-bench
```

## 6. Initialize the Bench Environment
Create a new directory called `frappe-bench` where all the code and sites will live. (We use version 15 here as the standard target, adjust if you are using v14).

```bash
cd ~
bench init frappe-bench --frappe-branch version-15
cd frappe-bench
```

## 7. Download Required Applications
Now we fetch the source code for ERPNext, HRMS, and your custom apps.

```bash
# Get Standard Apps
bench get-app payments
bench get-app erpnext --branch version-15
bench get-app hrms --branch version-15

# Get Custom Apps
# (Replace with your actual git repository URLs)
bench get-app jahan_kodak https://github.com/your-org/jahan_kodak.git
bench get-app jk_sync https://github.com/your-org/jk_sync.git
```

## 8. Create the Cloud Site
Create a new Frappe site. You will be prompted to enter your MariaDB root password, and to create an Administrator password for the ERPNext web UI.

```bash
export SITE_NAME="cloud.jahankodak.com"

bench new-site $SITE_NAME
```

## 9. Install Apps on the Cloud Site
Install the apps onto your newly created site. Order matters; ERPNext goes first.

```bash
bench --site $SITE_NAME install-app payments
bench --site $SITE_NAME install-app erpnext
bench --site $SITE_NAME install-app hrms
bench --site $SITE_NAME install-app jahan_kodak
bench --site $SITE_NAME install-app jk_sync
```

## 10. Configure Production (Nginx & Supervisor)
Transition the bench from a development state to a live production state.

```bash
sudo bench setup production frappe
```
*This command will automatically generate Nginx and Supervisor configuration files, link them to the system, and start the services.*

Ensure the site is set as default so Nginx knows where to route traffic:
```bash
bench use $SITE_NAME
```

## 11. Post-Deployment Steps
1. **Access the Site**: Open your browser and navigate to `http://cloud.jahankodak.com` (or your server's IP address).
2. **Login**: Use `Administrator` and the password you set in Step 8.
3. **Run Setup Wizard**: Complete the ERPNext setup wizard.
4. **Configure Sync**: Open `Branch Sync Config` and set up the API secrets for your physical branches so they can authenticate securely.

---
**Status**: The Cloud Server is now LIVE.
