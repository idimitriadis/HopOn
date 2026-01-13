import streamlit as st
import pandas as pd
import json
from utils.db import save_search, get_saved_searches, delete_search, get_users, create_user, delete_user
from utils.logger import logger

def reset_filters_to_defaults():
    """Sets all filter-related session state keys to their initial 'empty' state."""
    logger.info("Resetting filters to their default empty state.")
    st.session_state['filter_watchlist'] = False
    st.session_state['filter_start_date'] = None # Empty
    st.session_state['filter_end_date'] = None # Empty
    st.session_state['filter_clusters'] = [] # Empty
    st.session_state['filter_funding'] = [] # Empty
    st.session_state['filter_id'] = ""
    st.session_state['filter_objective'] = ""

def render_sidebar(projects):
    # --- Step 2 (Apply): Check for and apply a pending search load at the start of the run ---
    if 'search_to_load' in st.session_state:
        logger.info("Applying pending search load to session state.")
        filters = st.session_state.search_to_load
        
        # Apply the loaded state to the actual filter keys
        st.session_state.filter_watchlist = filters.get('show_watchlist', False)
        st.session_state.filter_start_date = pd.to_datetime(filters.get('start_date')).date() if filters.get('start_date') else None
        st.session_state.filter_clusters = filters.get('selected_clusters', [])
        st.session_state.filter_funding = filters.get('selected_funding_schemes', [])
        st.session_state.filter_id = filters.get('search_id', "")
        st.session_state.filter_objective = filters.get('search_objective', "")

        # Clean up the temporary key to prevent re-applying on the next rerun
        del st.session_state.search_to_load

    st.sidebar.header("User Profile")
    # ... (rest of the user management UI remains the same)
    
    # --- Profile Management and Filter Initialization ---
    # ...
    # (The following is a condensed representation of the existing user profile logic)
    users = get_users() 
    user_options = {u['username']: u['id'] for u in users}
    def on_user_change(): reset_filters_to_defaults()
    user_names = list(user_options.keys())
    try:
        index = user_names.index(st.session_state.get('newly_created_user', ''))
        del st.session_state['newly_created_user'] 
    except ValueError:
        index = 0
    selected_username = st.sidebar.selectbox("Current User", options=user_names, index=index, on_change=on_user_change, key="user_selector")
    if 'confirming_delete' not in st.session_state: st.session_state.confirming_delete = False
    if st.session_state.confirming_delete:
        if st.dialog(title=f"Delete User: {selected_username}?"):
            st.warning(f"Are you sure you want to permanently delete **{selected_username}**?")
            if st.button("Yes, Delete Permanently", type="primary"):
                delete_user(user_options[selected_username]); st.session_state.confirming_delete = False; on_user_change(); st.success(f"Deleted {selected_username}"); st.rerun()
        else:
            st.session_state.confirming_delete = False; st.rerun()
    with st.sidebar.popover("⚙️ Manage Profiles", use_container_width=True):
        new_username = st.text_input("New Username", key="new_user_input")
        if st.button("Create"):
            if new_username:
                if new_username in user_options: st.error("User exists.")
                else: create_user(new_username); st.session_state['newly_created_user'] = new_username; on_user_change(); st.rerun()
            else: st.warning("Enter name.")
        if selected_username:
            if st.button("Delete User", type="secondary"): st.session_state.confirming_delete = True; st.rerun()
    current_user_id = user_options.get(selected_username)
    st.session_state['current_user_id'] = current_user_id
    st.sidebar.markdown("---")
    st.sidebar.header("Project Filters")

    if projects.empty: return {}
    if 'filter_clusters' not in st.session_state: reset_filters_to_defaults()
    
    # --- Render Filter Widgets (Now safe to do) ---
    show_watchlist = st.sidebar.checkbox("Show Favorites Only", key='filter_watchlist')
    min_date = projects['startDate'].min(); max_date = projects['endDate'].max()
    start_date = st.sidebar.date_input("Start Date", min_value=min_date, max_value=max_date, key='filter_start_date', value=None)
    end_date = st.sidebar.date_input("End Date", min_value=min_date, max_value=max_date, key='filter_end_date', value=None)
    all_clusters = projects['cluster'].unique().tolist()
    selected_clusters = st.sidebar.multiselect("Select Clusters", options=all_clusters, key='filter_clusters')
    all_funding = projects['fundingScheme'].unique().tolist()
    selected_funding_schemes = st.sidebar.multiselect("Select Funding Schemes", options=all_funding, key='filter_funding')
    search_project_id = st.sidebar.text_input("Project ID", key='filter_id')
    search_objective = st.sidebar.text_input(
        "Semantic Search (Smart)", 
        key='filter_objective',
        help="Type a concept (e.g., 'Cancer', 'Green Energy'). AI will find relevant projects even if keywords don't match exactly."
    )

    # --- Saved Search UI ---
    if current_user_id:
        st.sidebar.subheader("Saved Searches")
        saved_searches = get_saved_searches(current_user_id)
        search_options = {s['name']: s for s in saved_searches}
        selected_search_name = st.sidebar.selectbox("Load Search", [""] + list(search_options.keys()))
        
        if selected_search_name:
            col_apply, col_del_search = st.sidebar.columns(2)
            with col_apply:
                # --- Step 1 (Request): Set the temporary key and rerun ---
                if st.button("Apply"):
                    search_data = search_options[selected_search_name]
                    filters = json.loads(search_data['filters'])
                    st.session_state['search_to_load'] = filters
                    st.rerun()
            with col_del_search:
                if st.button("Delete"):
                    delete_search(search_options[selected_search_name]['id']); st.rerun()

    # (Save Search and return logic remains the same)
    if current_user_id:
        with st.sidebar.expander("Save Current Search"):
            # ... (save logic)
            new_search_name = st.text_input("Name for this search")
            if st.button("Save Search"):
                if new_search_name:
                    current_filters = {
                        'show_watchlist': show_watchlist, 'start_date': str(start_date) if start_date else None,
                        'end_date': str(end_date) if end_date else None, 'selected_clusters': selected_clusters,
                        'selected_funding_schemes': selected_funding_schemes, 'search_id': search_project_id,
                        'search_objective': search_objective
                    }
                    save_search(new_search_name, json.dumps(current_filters), current_user_id)
                    st.rerun()
                else:
                    st.warning("Please enter a name.")
    
    return {
        'show_watchlist': show_watchlist, 'start_date': start_date, 'end_date': end_date,
        'selected_clusters': selected_clusters, 'selected_funding_schemes': selected_funding_schemes,
        'search_id': search_project_id, 'search_objective': search_objective, 'user_id': current_user_id
    }
