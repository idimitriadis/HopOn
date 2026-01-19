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

```table
ID    Username             Name                 Email
---------------------------------------------------------------------------
1     admin                Admin User           admin@example.com
2     researcher           Dr. Smith            smith@university.edu
```

### 2. Add a User

To create a new user:

```bash
python scripts/manage_users.py add <username> <password> [--name "Full Name"] [--email "email@addr.com"]
```

**Examples:**

```bash
# Minimal
python scripts/manage_users.py add john secret123

# Full Profile
python scripts/manage_users.py add maria securepass! --name "Maria Garcia" --email "maria@lab.eu"
```

### 3. Delete a User

(Currently manual deletion via database or python shell is required if not exposed in the script, see Phase 3).
**Note:** Deleting a user will also delete their Watchlist and Saved Searches.

## Database Migrations

If you modify the database schema (models), you must run migrations:

```bash
# Apply pending migrations
alembic upgrade head

# Create a new migration (after changing utils/models.py)
alembic revision --autogenerate -m "Description of change"
```
