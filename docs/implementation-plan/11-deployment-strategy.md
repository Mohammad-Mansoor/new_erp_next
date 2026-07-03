# 11. Deployment Strategy

This document describes the hosting architecture and commands required for production deployment.

### 1. Server Infrastructure
*   **Operating System:** Linux (Ubuntu 22.04 LTS recommended).
*   **Frappe Setup:** Standard multi-tenant bare-metal or Docker-containerized bench setup.
*   **Version Control:** Code managed in a private GitHub repository, separating custom developments into the `ziad_app` application.

### 2. Custom App Deployment Commands
To deploy customizations to the staging or production server:

```bash
# Fetch custom application from private repository
bench get-app https://github.com/your-org/ziad_app.git

# Install application onto the production site
bench --site production.example.com install-app ziad_app

# Run database migrations and build assets
bench --site production.example.com migrate
bench build
```

### 3. Backup and Disaster Recovery
*   **Automated Backups:** Run standard bench backups daily (database, files, and configurations).
*   **Cron Integration:** Sync backup archives to a secure off-site cloud storage bucket (e.g., AWS S3, Google Cloud Storage).
