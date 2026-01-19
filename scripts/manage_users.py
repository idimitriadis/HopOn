import argparse
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from utils.db import create_user, get_db, delete_user
from utils.models import User

def add_user(args):
    """Adds a new user (Simple)."""
    if not args.username or not args.username.strip():
        print("Error: Username cannot be empty.")
        return
    if not args.password or not args.password.strip():
        print("Error: Password cannot be empty.")
        return

    print(f"Creating user '{args.username}'...")
    # Name defaults to Username, Email is None
    user_id = create_user(args.username, args.password, name=args.username, email=None)
    if user_id:
        print(f"Success! User ID: {user_id}")
    else:
        print("Failed to create user (might already exist).")

def list_users(args):
    """Lists all users."""
    with get_db() as db:
        users = db.query(User).all()
        print(f"{'ID':<5} {'Username':<20} {'Name':<20}")
        print("-" * 50)
        for u in users:
            print(f"{u.id:<5} {u.username:<20} {u.name or '':<20}")

def delete_user_cli(args):
    """Deletes a user by Username."""
    with get_db() as db:
        user = db.query(User).filter(User.username == args.username).first()
        
        if not user:
            print(f"User '{args.username}' not found.")
            return

        if not args.yes:
            confirm = input(f"Delete user '{user.username}'? (y/N): ")
            if confirm.lower() != 'y':
                print("Cancelled.")
                return

        if delete_user(user.id):
            print(f"User '{user.username}' deleted.")
        else:
            print("Failed.")

def main():
    parser = argparse.ArgumentParser(description="HopOn Simple Admin CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ADD
    add_parser = subparsers.add_parser("add", help="Create a new user")
    add_parser.add_argument("username", help="Login Username")
    add_parser.add_argument("password", help="Login Password")
    add_parser.set_defaults(func=add_user)

    # LIST
    list_parser = subparsers.add_parser("list", help="Show all users")
    list_parser.set_defaults(func=list_users)

    # DELETE
    del_parser = subparsers.add_parser("delete", help="Remove a user")
    del_parser.add_argument("username", help="Username to delete")
    del_parser.add_argument("-y", "--yes", action="store_true", help="Skip check")
    del_parser.set_defaults(func=delete_user_cli)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
