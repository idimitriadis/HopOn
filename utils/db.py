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
# pool_pre_ping=True helps with connection stability
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
    """
    Initializes the database. 
    Now primarily used to ensure the file exists or for initial seeding if needed.
    Migrations (Alembic) handle the schema.
    """
    logger.info(f"Database engine initialized at {DB_URL}")
    # We could seed the default user here if missing, ensuring they have a password
    seed_default_admin()

def seed_default_admin():
    with get_db() as db:
        admin = db.query(User).filter(User.username == "Vasilis").first()
        if not admin:
            # Default password: admin
            # Generated with bcrypt.hashpw(b"admin", bcrypt.gensalt()).decode()
            hashed_pw = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
            new_admin = User(username="Vasilis", name="Admin", password_hash=hashed_pw)
            db.add(new_admin)
            db.commit()
            logger.info("Seeded default admin user 'Vasilis'")

# --- User Management ---
def create_user(username, password, name=None, email=None):
    """Creates a new user with a hashed password."""
    # Hash the password
    # bcrypt requires bytes
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
        user = db.query(User).filter(User.username == "Vasilis").first()
        if not user:
            return False
        
        # Check password
        return bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8'))

def get_all_users_config():
    """
    Returns a dictionary of users formatted for streamlit-authenticator.
    {'usernames': {'user1': {'email':.., 'name':.., 'password':..}}}
    """
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
            # Check if exists
            exists = db.query(Watchlist).filter_by(project_id=project_id, user_id=user_id).first()
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
# (Keeping simple for now, can be refactored similarly if needed)