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
        # Watchlist table
        c.execute('''CREATE TABLE IF NOT EXISTS watchlist
                     (project_id TEXT PRIMARY KEY, added_at TIMESTAMP)''')
        
        # Saved Searches table
        c.execute('''CREATE TABLE IF NOT EXISTS saved_searches
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, filters TEXT, created_at TIMESTAMP)''')
        
        conn.commit()
        logger.success("Database tables initialized/verified.")
    except sqlite3.Error as e:
        logger.exception(f"Error initializing database: {e}")
    finally:
        conn.close()

def add_to_watchlist(project_id, db_path=DEFAULT_DB_PATH):
    conn = get_connection(db_path)
    c = conn.cursor()
    try:
        c.execute("INSERT OR IGNORE INTO watchlist (project_id, added_at) VALUES (?, ?)", 
                  (project_id, datetime.now().isoformat()))
        conn.commit()
        logger.info(f"Added project {project_id} to watchlist.")
    except sqlite3.Error as e:
        logger.exception(f"Error adding {project_id} to watchlist: {e}")
    finally:
        conn.close()

def remove_from_watchlist(project_id, db_path=DEFAULT_DB_PATH):
    conn = get_connection(db_path)
    c = conn.cursor()
    try:
        c.execute("DELETE FROM watchlist WHERE project_id = ?", (project_id,))
        conn.commit()
        logger.info(f"Removed project {project_id} from watchlist.")
    except sqlite3.Error as e:
        logger.exception(f"Error removing {project_id} from watchlist: {e}")
    finally:
        conn.close()

def get_watchlist(db_path=DEFAULT_DB_PATH):
    conn = get_connection(db_path)
    c = conn.cursor()
    try:
        c.execute("SELECT project_id FROM watchlist")
        rows = c.fetchall()
        return [row[0] for row in rows]
    except sqlite3.Error as e:
        logger.exception(f"Error fetching watchlist: {e}")
        return []
    finally:
        conn.close()

def save_search(name, filters, db_path=DEFAULT_DB_PATH):
    conn = get_connection(db_path)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO saved_searches (name, filters, created_at) VALUES (?, ?, ?)",
                  (name, filters, datetime.now().isoformat()))
        conn.commit()
        logger.info(f"Saved search '{name}'.")
    except sqlite3.Error as e:
        logger.exception(f"Error saving search '{name}': {e}")
    finally:
        conn.close()

def get_saved_searches(db_path=DEFAULT_DB_PATH):
    conn = get_connection(db_path)
    conn.row_factory = sqlite3.Row # Access columns by name
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM saved_searches ORDER BY created_at DESC")
        rows = c.fetchall()
        # Convert sqlite3.Row to dict
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
