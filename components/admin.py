import streamlit as st
from utils.db import create_user, delete_user, update_user, get_db
from utils.models import User

def render_admin_panel(current_user_id):
    """
    Renders the User Management interface for logged-in users.
    """
    st.header("👥 User Management")
    st.info("You can manage application access here.")

    tab_list, tab_add, tab_edit = st.tabs(["List / Delete Users", "Add New User", "Edit User"])

    # --- TAB 1: LIST & DELETE ---
    with tab_list:
        with get_db() as db:
            users = db.query(User).all()
            data = [{'ID': u.id, 'Username': u.username, 'Created At': u.created_at} for u in users]
        
        if data:
            st.dataframe(data, use_container_width=True, hide_index=True)
            
            st.subheader("Remove Access")
            user_to_delete = st.selectbox("Select User to Delete", options=users, format_func=lambda x: x.username)
            
            if user_to_delete:
                if user_to_delete.id == current_user_id:
                    st.warning("⚠️ You are selecting yourself. Deleting will log you out.")
                
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
            submitted = st.form_submit_button("Create User")
            
            if submitted:
                if new_username and new_password:
                    uid = create_user(new_username, new_password, name=new_username, email=None)
                    if uid:
                        st.success(f"User '{new_username}' created successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to create user.")
                else:
                    st.warning("Username and Password are required.")

    # --- TAB 3: EDIT USER ---
    with tab_edit:
        st.subheader("Update Credentials")
        # Reuse users list from Tab 1 context or re-fetch if needed (safe to re-use if within same render)
        # But for correctness with selectbox state, accessing the list variable is fine.
        
        user_to_edit = st.selectbox("Select User to Edit", options=users, format_func=lambda x: x.username, key="user_edit_select")
        
        if user_to_edit:
            with st.form("edit_user_form"):
                st.caption(f"Editing: **{user_to_edit.username}**")
                edit_username = st.text_input("New Username (leave blank to keep current)")
                edit_password = st.text_input("New Password (leave blank to keep current)", type="password")
                
                update_submitted = st.form_submit_button("Update User")
                
                if update_submitted:
                    if not edit_username and not edit_password:
                        st.warning("No changes entered.")
                    else:
                        success = update_user(
                            user_to_edit.id, 
                            new_username=edit_username if edit_username else None,
                            new_password=edit_password if edit_password else None
                        )
                        if success:
                            st.success("User updated successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to update user.")
