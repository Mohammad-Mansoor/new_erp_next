# Provisioning a New Branch Local Server

This guide explains the exact step-by-step workflow for setting up a brand new Local Server for an additional branch by cloning the Production (Cloud) Server data. 

This process assumes that the local computer already has Ubuntu installed, Frappe/ERPNext prerequisites set up, and the `frappe-bench` directory initialized with the `jahan_kodak` and `jk_sync` apps downloaded. If the local site data is corrupted or it's a completely blank slate, this workflow will guarantee a clean, exact replica of your Cloud Server.

---

## Step 1: Take a Full Backup on the Cloud (VPS) Server

You need a complete snapshot of your production data. Log into your Cloud Server via SSH, navigate to your `frappe-bench` directory, and run a full backup including files:

```bash
cd frappe-bench
bench --site [your_cloud_site_name] backup --with-files
```

This command will generate three essential files in the `sites/[your_cloud_site_name]/private/backups/` directory:
1. **Database backup** (e.g., `20261008_...-database.sql.gz`)
2. **Public files** (e.g., `20261008_...-files.tar`)
3. **Private files** (e.g., `20261008_...-private-files.tar`)

---

## Step 2: Transfer the Backups to the New Local Server

Download those three generated files from your Cloud Server and transfer them to your new Local Server computer. 

*Tip: You can use `scp` or a tool like FileZilla to securely download the files from the VPS. Once downloaded, move them to a convenient folder on your local computer (e.g., inside `frappe-bench/backups/`).*

---

## Step 3: Wipe the Corrupted Site (Clean Slate)

To avoid any lingering bugs or corrupted data, you should destroy the existing corrupted database and recreate a fresh, empty site. 

Open your terminal on the **Local Server**, navigate to `frappe-bench`, and run:

```bash
# 1. Drop the corrupted site (WARNING: this completely deletes the local database)
bench drop-site [your_local_site_name] --force

# 2. Create a fresh, clean site with the same name
bench new-site [your_local_site_name]

# 3. Install the required apps onto this empty site
bench --site [your_local_site_name] install-app erpnext jahan_kodak jk_sync
```

---

## Step 4: Restore the Cloud Backup to the Local Server

Now, you will inject the data from your Cloud Server into the fresh local site using the backup files you transferred in Step 2.

Run the restore command, replacing the file paths with the exact locations of your backup files:

```bash
bench --site [your_local_site_name] restore /path/to/database.sql.gz \
    --with-public-files /path/to/files.tar \
    --with-private-files /path/to/private-files.tar
```

---

## Step 5: Migrate and Finalize

After the restore is complete, it is absolutely critical to run a database migration. This ensures all the database tables are perfectly aligned with the Python and JavaScript codebase of your apps.

```bash
bench --site [your_local_site_name] migrate
```

---

## Step 6: Configure the Branch Sync Settings

At this point, your Local Server is a 100% perfect clone of the Cloud Server. **This means it currently thinks it is the Cloud Server!** You must configure it so it acts as a separate branch.

1. Log in to your Local Server's ERPNext instance in your web browser.
2. Search for **Branch Sync Config** and open the configuration.
3. Change the **Branch Name** to your new branch (e.g., "Branch 2" or "Karteh Naw").
4. Ensure the **Local Server URL** points to this machine (e.g., `http://127.0.0.1:8000`).
5. Ensure the **Cloud Server URL** is pointing to your production VPS.
6. **Create a new Sync User:** Go to your Cloud Server, create a new User specifically for this branch (e.g., `sync_user_branch2@jahan.com`), and generate API Keys for them. 
7. Enter those new API keys into the Branch Sync Config on your Local Server.

Your new Local Server is now fully provisioned and ready to start syncing data exclusively for this branch!
