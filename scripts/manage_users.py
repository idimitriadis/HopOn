import argparse
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from utils.db import create_user, get_db
from utils.models import User

def add_user(args):
    """Adds a new user."""
    print(f"Creating user '{args.username}'...")
    user_id = create_user(args.username, args.password, args.name, args.email)
    if user_id:
        print(f"Success! User ID: {user_id}")
    else:
        print("Failed to create user (might already exist).")

def list_users(args):
    """Lists all users."""
    with get_db() as db:
        users = db.query(User).all()
        print(f"{'ID':<5} {'Username':<20} {'Name':<20} {'Email':<30}")
        print("-" * 75)
        for u in users:
            print(f"{u.id:<5} {u.username:<20} {u.name or '':<20} {u.email or '':<30}")

def main():
    parser = argparse.ArgumentParser(description="HopOn User Management")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add User Command
    add_parser = subparsers.add_parser("add", help="Add a new user")
    add_parser.add_argument("username", help="Username for login")
    add_parser.add_argument("password", help="Password")
    add_parser.add_argument("--name", help="Full Name (optional)")
    add_parser.add_argument("--email", help="Email (optional)")
    add_parser.set_defaults(func=add_user)

    # List Users Command
    list_parser = subparsers.add_parser("list", help="List all users")
    list_parser.set_defaults(func=list_users)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
