import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from utils.models import Base, User, Watchlist, SavedSearch
from utils.logger import logger
from dotenv import load_dotenv
import bcrypt

load_dotenv()

# Database Setup
DB_URL = os.getenv("DATABASE_URL", "sqlite:///data/db/user_prefs.db")

# Create Engine
engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if "sqlite" in DB_URL else {})

# Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    """Context manager for database sessions."""
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def init_db():
    """Initializes the database."""
    logger.info(f"Database engine initialized at {DB_URL}")
    seed_default_admin()

def seed_default_admin():
    with get_db() as db:
        admin = db.query(User).filter(User.username == "Vasilis").first()
        if not admin:
            # Default password: admin
            hashed_pw = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
            new_admin = User(username="Vasilis", name="Admin", password_hash=hashed_pw)
            db.add(new_admin)
            db.commit()
            logger.info("Seeded default admin user 'Vasilis'")

# --- User Management ---
def create_user(username, password, name=None, email=None):
    """Creates a new user with a hashed password."""
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

    with get_db() as db:
        try:
            user = User(username=username, password_hash=hashed, name=name, email=email)
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"Created new user: {username}")
            return user.id
        except Exception as e:
            logger.error(f"Error creating user {username}: {e}")
            return None

def verify_user(username, password):
    """Verifies a user's credentials."""
    with get_db() as db:
        # BUG FIXED: Was hardcoded to "Vasilis"
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return False
        
        return bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8'))

def get_all_users_config():
    with get_db() as db:
        users = db.query(User).all()
        config = {}
        for u in users:
            config[u.username] = {
                'email': u.email,
                'name': u.name or u.username,
                'password': u.password_hash
            }
        return config

def get_user_id(username):
    with get_db() as db:
        user = db.query(User).filter(User.username == username).first()
        return user.id if user else None

# --- Watchlist ---
def add_to_watchlist(project_id, user_id):
    with get_db() as db:
        try:
            exists = db.query(Watchlist).filter_by(project_id=str(project_id), user_id=user_id).first()
            if not exists:
                item = Watchlist(project_id=str(project_id), user_id=user_id)
                db.add(item)
                db.commit()
                logger.info(f"User {user_id}: Added {project_id} to watchlist.")
        except Exception as e:
            logger.error(f"Error adding to watchlist: {e}")

def remove_from_watchlist(project_id, user_id):
    with get_db() as db:
        db.query(Watchlist).filter_by(project_id=str(project_id), user_id=user_id).delete()
        db.commit()
        logger.info(f"User {user_id}: Removed {project_id} from watchlist.")

def get_watchlist(user_id):
    with get_db() as db:
        items = db.query(Watchlist).filter(Watchlist.user_id == user_id).all()
        return [item.project_id for item in items]

# --- Saved Searches ---
def save_search(name, filters_json, user_id):
    with get_db() as db:
        try:
            search = SavedSearch(name=name, filters=filters_json, user_id=user_id)
            db.add(search)
            db.commit()
            logger.info(f"User {user_id}: Saved search '{name}'")
        except Exception as e:
            logger.error(f"Error saving search: {e}")

def get_saved_searches(user_id):
    with get_db() as db:
        items = db.query(SavedSearch).filter(SavedSearch.user_id == user_id).order_by(SavedSearch.created_at.desc()).all()
        # Convert to dict for compatibility
        return [{'id': item.id, 'name': item.name, 'filters': item.filters, 'created_at': item.created_at} for item in items]

def delete_search(search_id):
    with get_db() as db:
        try:
            db.query(SavedSearch).filter(SavedSearch.id == search_id).delete()
            db.commit()
            logger.info(f"Deleted search {search_id}")
        except Exception as e:
            logger.error(f"Error deleting search: {e}")

def delete_user(user_id):
    """Deletes user and cascades via ORM relationships."""
    with get_db() as db:
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                db.delete(user) # Cascade deletes watchlist/searches defined in Model
                db.commit()
                logger.info(f"Deleted user {user_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            return False
