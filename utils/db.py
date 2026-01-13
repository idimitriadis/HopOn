import sqlite3
import os
from datetime import datetime
from utils.logger import logger

# Default path relative to the project root
DEFAULT_DB_PATH = os.path.join("data", "db", "user_prefs.db")

def get_connection(db_path):
    # Ensure directory exists
    directory = os.path.dirname(db_path)
    if directory and not os.path.exists(directory):
        try:
            os.makedirs(directory)
            logger.info(f"Created database directory: {directory}")
        except OSError as e:
            logger.error(f"Failed to create database directory {directory}: {e}")
            raise

    return sqlite3.connect(db_path)

def init_db(db_path=DEFAULT_DB_PATH):
    logger.info(f"Initializing database at {db_path}")
    conn = get_connection(db_path)
    c = conn.cursor()
    
    try:
        # Enable Foreign Keys
        c.execute("PRAGMA foreign_keys = ON")

        # Users table
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE)''')

        # Watchlist table (added user_id)
        c.execute('''CREATE TABLE IF NOT EXISTS watchlist
                     (project_id TEXT, 
                      user_id INTEGER,
                      added_at TIMESTAMP,
                      PRIMARY KEY (project_id, user_id),
                      FOREIGN KEY(user_id) REFERENCES users(id))''')
        
        # Saved Searches table (added user_id)
        c.execute('''CREATE TABLE IF NOT EXISTS saved_searches
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      user_id INTEGER,
                      name TEXT, 
                      filters TEXT, 
                      created_at TIMESTAMP,
                      FOREIGN KEY(user_id) REFERENCES users(id))''')
        
        # Seed Default User if empty
        c.execute("SELECT count(*) FROM users")
        if c.fetchone()[0] == 0:
            c.execute("INSERT INTO users (username) VALUES (?)", ("Vasilis",))
            logger.info("Seeded default user 'Vasilis'")
        
        conn.commit()
        logger.success("Database tables initialized/verified.")
    except sqlite3.Error as e:
        logger.exception(f"Error initializing database: {e}")
    finally:
        conn.close()

# --- User Management ---
def create_user(username, db_path=DEFAULT_DB_PATH):
    conn = get_connection(db_path)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()
        logger.info(f"Created new user: {username}")
        return c.lastrowid
    except sqlite3.IntegrityError:
        logger.warning(f"User {username} already exists.")
        return None
    except sqlite3.Error as e:
        logger.exception(f"Error creating user {username}: {e}")
        return None
    finally:
        conn.close()

def delete_user(user_id, db_path=DEFAULT_DB_PATH):
    conn = get_connection(db_path)
    c = conn.cursor()
    try:
        # Manual Cascade Deletion
        c.execute("DELETE FROM watchlist WHERE user_id = ?", (user_id,))
        c.execute("DELETE FROM saved_searches WHERE user_id = ?", (user_id,))
        c.execute("DELETE FROM users WHERE id = ?", (user_id,))
        
        conn.commit()
        logger.info(f"Deleted user {user_id} and all associated data.")
        return True
    except sqlite3.Error as e:
        logger.exception(f"Error deleting user {user_id}: {e}")
        return False
    finally:
        conn.close()

def get_users(db_path=DEFAULT_DB_PATH):
    conn = get_connection(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM users ORDER BY username")
        return [dict(row) for row in c.fetchall()]
    finally:
        conn.close()

def get_user_id(username, db_path=DEFAULT_DB_PATH):
    conn = get_connection(db_path)
    c = conn.cursor()
    try:
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        row = c.fetchone()
        return row[0] if row else None
    finally:
        conn.close()

# --- Watchlist ---
def add_to_watchlist(project_id, user_id, db_path=DEFAULT_DB_PATH):
    conn = get_connection(db_path)
    c = conn.cursor()
    try:
        c.execute("INSERT OR IGNORE INTO watchlist (project_id, user_id, added_at) VALUES (?, ?, ?)", 
                  (project_id, user_id, datetime.now().isoformat()))
        conn.commit()
        logger.info(f"User {user_id}: Added project {project_id} to watchlist.")
    except sqlite3.Error as e:
        logger.exception(f"Error adding {project_id} to watchlist: {e}")
    finally:
        conn.close()

def remove_from_watchlist(project_id, user_id, db_path=DEFAULT_DB_PATH):
    conn = get_connection(db_path)
    c = conn.cursor()
    try:
        c.execute("DELETE FROM watchlist WHERE project_id = ? AND user_id = ?", (project_id, user_id))
        conn.commit()
        logger.info(f"User {user_id}: Removed project {project_id} from watchlist.")
    except sqlite3.Error as e:
        logger.exception(f"Error removing {project_id} from watchlist: {e}")
    finally:
        conn.close()

def get_watchlist(user_id, db_path=DEFAULT_DB_PATH):
    conn = get_connection(db_path)
    c = conn.cursor()
    try:
        c.execute("SELECT project_id FROM watchlist WHERE user_id = ?", (user_id,))
        rows = c.fetchall()
        return [row[0] for row in rows]
    except sqlite3.Error as e:
        logger.exception(f"Error fetching watchlist: {e}")
        return []
    finally:
        conn.close()

# --- Saved Searches ---
def save_search(name, filters, user_id, db_path=DEFAULT_DB_PATH):
    conn = get_connection(db_path)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO saved_searches (name, filters, user_id, created_at) VALUES (?, ?, ?, ?)",
                  (name, filters, user_id, datetime.now().isoformat()))
        conn.commit()
        logger.info(f"User {user_id}: Saved search '{name}'.")
    except sqlite3.Error as e:
        logger.exception(f"Error saving search '{name}': {e}")
    finally:
        conn.close()

def get_saved_searches(user_id, db_path=DEFAULT_DB_PATH):
    conn = get_connection(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM saved_searches WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        rows = c.fetchall()
        return [dict(zip(row.keys(), row)) for row in rows]
    except sqlite3.Error as e:
        logger.exception(f"Error fetching saved searches: {e}")
        return []
    finally:
        conn.close()

def delete_search(search_id, db_path=DEFAULT_DB_PATH):
    conn = get_connection(db_path)
    c = conn.cursor()
    try:
        c.execute("DELETE FROM saved_searches WHERE id = ?", (search_id,))
        conn.commit()
        logger.info(f"Deleted search with ID {search_id}.")
    except sqlite3.Error as e:
        logger.exception(f"Error deleting search ID {search_id}: {e}")
    finally:
        conn.close()
