import streamlit as st
import pandas as pd

def render_sidebar(projects):
    st.sidebar.header("Project Filters")

    if projects.empty:
        return {}
    
    # Watchlist toggle
    show_watchlist = st.sidebar.checkbox("Show Favorites Only")

    min_date = projects['startDate'].min()
    max_date = projects['endDate'].max()
    
    # Logic from app.py
    min_end_date = max(projects['endDate'].min(), pd.to_datetime("2027-09-25"))

    # Date range filter
    start_date = st.sidebar.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.sidebar.date_input("End Date", min_value=min_end_date, max_value=max_date, value=max_date)

    # Cluster filter
    clusters = projects['cluster'].unique().tolist()
    selected_clusters = st.sidebar.multiselect("Select Clusters", options=clusters, default=clusters)

    # Funding scheme filter
    funding_schemes = projects['fundingScheme'].unique().tolist()
    selected_funding_schemes = st.sidebar.multiselect("Select Funding Schemes", options=funding_schemes,
                                                      default=funding_schemes)
    
    search_project_id = st.sidebar.text_input("Project ID")
    # Objective Keyword search
    search_objective = st.sidebar.text_input("Search Objective")

    return {
        'show_watchlist': show_watchlist,
        'start_date': start_date,
        'end_date': end_date,
        'selected_clusters': selected_clusters,
        'selected_funding_schemes': selected_funding_schemes,
        'search_id': search_project_id,
        'search_objective': search_objective
    }
