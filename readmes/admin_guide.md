# Administrator's Guide

This guide explains how to manage users in HopOn using the Command Line Interface (CLI).

## User Management Script

All user management is performed using the `scripts/manage_users.py` script. This ensures that passwords are securely hashed before being stored in the database.

**Prerequisite:** Ensure your virtual environment is activated.

### 1. List Users
To see all registered users:
```bash
python scripts/manage_users.py list
```

**Output:**
```
ID    Username             Name
--------------------------------------------------
1     admin                admin
2     researcher           researcher
```

### 2. Add a User
To create a new user (Username and Password are required):
```bash
python scripts/manage_users.py add <username> <password>
```

**Example:**
```bash
python scripts/manage_users.py add admin mysecurepassword
```
*(The Name will default to the Username. You can edit profile details inside the app later if needed.)*

### 3. Delete a User
To delete a user and their data:
```bash
python scripts/manage_users.py delete <username>
```

**Example:**
```bash
python scripts/manage_users.py delete admin
```
*(You will be asked to confirm unless you add `-y`)*

## Database Migrations
If you modify the database schema (models), you must run migrations:

```bash
# Apply pending migrations
alembic upgrade head
```