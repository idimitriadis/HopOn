import streamlit as st
import pandas as pd
import json
from utils.db import save_search, get_saved_searches, delete_search
from utils.logger import logger

def render_sidebar(projects):
    st.sidebar.header("Project Filters")

    if projects.empty:
        return {}

    # --- 1. Session State Initialization ---
    # We use specific keys for our widgets. If they don't exist, we set defaults.
    
    # Defaults
    default_clusters = projects['cluster'].unique().tolist()
    default_funding = projects['fundingScheme'].unique().tolist()
    min_date = projects['startDate'].min()
    max_date = projects['endDate'].max()
    min_end_date = max(projects['endDate'].min(), pd.to_datetime("2027-09-25"))

    if 'filter_watchlist' not in st.session_state:
        st.session_state['filter_watchlist'] = False
    if 'filter_start_date' not in st.session_state:
        st.session_state['filter_start_date'] = min_date
    if 'filter_end_date' not in st.session_state:
        st.session_state['filter_end_date'] = max_date
    if 'filter_clusters' not in st.session_state:
        st.session_state['filter_clusters'] = default_clusters
    if 'filter_funding' not in st.session_state:
        st.session_state['filter_funding'] = default_funding
    if 'filter_id' not in st.session_state:
        st.session_state['filter_id'] = ""
    if 'filter_objective' not in st.session_state:
        st.session_state['filter_objective'] = ""

    # --- 2. Saved Search UI (Load) ---
    st.sidebar.subheader("Saved Searches")
    saved_searches = get_saved_searches()
    
    # Create options dict for dropdown {name: id}
    search_options = {s['name']: s for s in saved_searches}
    selected_search_name = st.sidebar.selectbox(
        "Load Search", 
        options=[""] + list(search_options.keys()),
        index=0,
        key="load_search_dropdown" # Separate key to avoid conflicts
    )
    
    # Load Logic
    if selected_search_name and selected_search_name != "":
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("Apply"):
                search_data = search_options[selected_search_name]
                try:
                    filters = json.loads(search_data['filters'])
                    
                    # Update Session State
                    st.session_state['filter_watchlist'] = filters.get('show_watchlist', False)
                    
                    # Handle dates (convert string back to date object if needed, though date_input handles iso strings often)
                    # Ideally we cast to date objects to be safe
                    if filters.get('start_date'):
                        st.session_state['filter_start_date'] = pd.to_datetime(filters['start_date']).date()
                    if filters.get('end_date'):
                        st.session_state['filter_end_date'] = pd.to_datetime(filters['end_date']).date()
                        
                    st.session_state['filter_clusters'] = filters.get('selected_clusters', default_clusters)
                    st.session_state['filter_funding'] = filters.get('selected_funding_schemes', default_funding)
                    st.session_state['filter_id'] = filters.get('search_id', "")
                    st.session_state['filter_objective'] = filters.get('search_objective', "")
                    
                    logger.info(f"Applied saved search: {selected_search_name}")
                    st.rerun()
                except Exception as e:
                    logger.error(f"Failed to load search: {e}")
                    st.error("Error loading search.")
        
        with col2:
            if st.button("Delete"):
                search_id = search_options[selected_search_name]['id']
                delete_search(search_id)
                st.success(f"Deleted '{selected_search_name}'")
                st.rerun()

    # --- 3. Filter Widgets ---
    # Watchlist toggle
    show_watchlist = st.sidebar.checkbox("Show Favorites Only", key='filter_watchlist')

    # Date range filter
    start_date = st.sidebar.date_input("Start Date", min_value=min_date, max_value=max_date, key='filter_start_date')
    end_date = st.sidebar.date_input("End Date", min_value=min_end_date, max_value=max_date, key='filter_end_date')

    # Cluster filter
    selected_clusters = st.sidebar.multiselect("Select Clusters", options=default_clusters, key='filter_clusters')

    # Funding scheme filter
    selected_funding_schemes = st.sidebar.multiselect("Select Funding Schemes", options=default_funding, key='filter_funding')
    
    search_project_id = st.sidebar.text_input("Project ID", key='filter_id')
    # Objective Keyword search
    search_objective = st.sidebar.text_input("Search Objective", key='filter_objective')

    # --- 4. Save Search UI ---
    st.sidebar.markdown("---")
    with st.sidebar.expander("Save Current Search"):
        new_search_name = st.text_input("Name for this search")
        if st.button("Save Search"):
            if new_search_name:
                # Serialize filters
                current_filters = {
                    'show_watchlist': show_watchlist,
                    'start_date': str(start_date),
                    'end_date': str(end_date),
                    'selected_clusters': selected_clusters,
                    'selected_funding_schemes': selected_funding_schemes,
                    'search_id': search_project_id,
                    'search_objective': search_objective
                }
                save_search(new_search_name, json.dumps(current_filters))
                st.success(f"Saved: {new_search_name}")
                st.rerun() # Rerun to update the Load dropdown
            else:
                st.warning("Please enter a name.")

    return {
        'show_watchlist': show_watchlist,
        'start_date': start_date,
        'end_date': end_date,
        'selected_clusters': selected_clusters,
        'selected_funding_schemes': selected_funding_schemes,
        'search_id': search_project_id,
        'search_objective': search_objective
    }
