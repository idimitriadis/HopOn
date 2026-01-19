import streamlit as st
from utils.db import create_user, delete_user, get_all_users_config
from utils.models import User
from utils.db import get_db

def render_admin_panel(current_user_id):
    """
    Renders the User Management interface for logged-in users.
    """
    st.header("👥 User Management")
    st.info("You can manage application access here.")

    tab_list, tab_add = st.tabs(["List / Delete Users", "Add New User"])

    # --- TAB 1: LIST & DELETE ---
    with tab_list:
        # Fetch users directly for display
        with get_db() as db:
            users = db.query(User).all()
            
            # Convert to DataFrame for a nice table
            data = [{
                'ID': u.id, 
                'Username': u.username, 
                'Name': u.name, 
                'Email': u.email,
                'Created At': u.created_at
            } for u in users]
        
        if data:
            st.dataframe(data, use_container_width=True, hide_index=True)
            
            st.subheader("Remove Access")
            user_to_delete = st.selectbox("Select User to Delete", options=users, format_func=lambda x: f"{x.username} ({x.name})")
            
            if user_to_delete:
                # Prevent self-deletion if you want, though valid for testing
                if user_to_delete.id == current_user_id:
                    st.warning("⚠️ You are selecting yourself. If you delete this, you will be logged out immediately.")
                
                if st.button("🗑️ Delete User", type="primary"):
                    if delete_user(user_to_delete.id):
                        st.success(f"User {user_to_delete.username} deleted.")
                        st.rerun()
                    else:
                        st.error("Failed to delete user.")

    # --- TAB 2: ADD USER ---
    with tab_add:
        st.subheader("Create New Account")
        with st.form("create_user_form"):
            new_username = st.text_input("Username*")
            new_password = st.text_input("Password*", type="password")
            new_name = st.text_input("Full Name")
            # Email optional
            
            submitted = st.form_submit_button("Create User")
            
            if submitted:
                if new_username and new_password:
                    # Check if exists (basic check)
                    # create_user handles the hashing and DB insertion
                    uid = create_user(new_username, new_password, new_name)
                    
                    if uid:
                        st.success(f"User '{new_username}' created successfully!")
                        st.rerun() # Refresh to show in list
                    else:
                        st.error("Failed to create user. Username might already be taken.")
                else:
                    st.warning("Username and Password are required.")
