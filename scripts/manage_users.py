import argparse
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from utils.db import create_user, get_db, delete_user
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

def delete_user_cli(args):
    """Deletes a user by Username or ID."""
    with get_db() as db:
        user = None
        if args.id:
            user = db.query(User).filter(User.id == int(args.id)).first()
        elif args.username:
            user = db.query(User).filter(User.username == args.username).first()
        
        if not user:
            print("User not found.")
            return

        if not args.yes:
            confirm = input(f"Are you sure you want to delete user '{user.username}' and ALL their data? (y/N): ")
            if confirm.lower() != 'y':
                print("Operation cancelled.")
                return

        if delete_user(user.id):
            print(f"User '{user.username}' deleted.")
        else:
            print("Failed to delete user.")

def main():
    parser = argparse.ArgumentParser(description="HopOn User Management")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add User
    add_parser = subparsers.add_parser("add", help="Add a new user")
    add_parser.add_argument("username", help="Username")
    add_parser.add_argument("password", help="Password")
    add_parser.add_argument("--name", help="Full Name")
    add_parser.add_argument("--email", help="Email")
    add_parser.set_defaults(func=add_user)

    # List Users
    list_parser = subparsers.add_parser("list", help="List all users")
    list_parser.set_defaults(func=list_users)

    # Delete User
    del_parser = subparsers.add_parser("delete", help="Delete a user")
    group = del_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--username", help="Username to delete")
    group.add_argument("--id", help="User ID to delete")
    del_parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmation")
    del_parser.set_defaults(func=delete_user_cli)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()