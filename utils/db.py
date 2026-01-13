import sqlite3
from datetime import datetime

def get_connection(db_path):
    return sqlite3.connect(db_path)

def init_db(db_path='user_prefs.db'):
    conn = get_connection(db_path)
    c = conn.cursor()
    
    # Watchlist table
    c.execute('''CREATE TABLE IF NOT EXISTS watchlist
                 (project_id TEXT PRIMARY KEY, added_at TIMESTAMP)''')
    
    # Saved Searches table
    c.execute('''CREATE TABLE IF NOT EXISTS saved_searches
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, filters TEXT, created_at TIMESTAMP)''')
    
    conn.commit()
    conn.close()

def add_to_watchlist(project_id, db_path='user_prefs.db'):
    conn = get_connection(db_path)
    c = conn.cursor()
    try:
        c.execute("INSERT OR IGNORE INTO watchlist (project_id, added_at) VALUES (?, ?)", 
                  (project_id, datetime.now().isoformat()))
        conn.commit()
    finally:
        conn.close()

def remove_from_watchlist(project_id, db_path='user_prefs.db'):
    conn = get_connection(db_path)
    c = conn.cursor()
    try:
        c.execute("DELETE FROM watchlist WHERE project_id = ?", (project_id,))
        conn.commit()
    finally:
        conn.close()

def get_watchlist(db_path='user_prefs.db'):
    conn = get_connection(db_path)
    c = conn.cursor()
    try:
        c.execute("SELECT project_id FROM watchlist")
        rows = c.fetchall()
        return [row[0] for row in rows]
    finally:
        conn.close()

def save_search(name, filters, db_path='user_prefs.db'):
    conn = get_connection(db_path)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO saved_searches (name, filters, created_at) VALUES (?, ?, ?)",
                  (name, filters, datetime.now().isoformat()))
        conn.commit()
    finally:
        conn.close()

def get_saved_searches(db_path='user_prefs.db'):
    conn = get_connection(db_path)
    conn.row_factory = sqlite3.Row # Access columns by name
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM saved_searches ORDER BY created_at DESC")
        rows = c.fetchall()
        # Convert sqlite3.Row to dict
        return [dict(zip(row.keys(), row)) for row in rows]
    finally:
        conn.close()

def delete_search(search_id, db_path='user_prefs.db'):
    conn = get_connection(db_path)
    c = conn.cursor()
    try:
        c.execute("DELETE FROM saved_searches WHERE id = ?", (search_id,))
        conn.commit()
    finally:
        conn.close()
