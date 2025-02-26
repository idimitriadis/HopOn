import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="HopOn Projects", layout="wide")

@st.cache_data
def load_projects():
    projects = pd.read_csv('projects.csv',delimiter='|')
    projects['startDate'] = pd.to_datetime(projects['startDate'],errors='coerce')
    projects['endDate'] = pd.to_datetime(projects['endDate'], errors='coerce')
    projects['id'] = projects['id'].astype('str')
    return projects

@st.cache_data
def load_orgs():
    orgs = pd.read_csv('orgs.csv',delimiter='|')
    orgs['projectID'] = orgs['projectID'].astype('str')
    return orgs

# Title
st.title("Available Hopon Projects")
projects = load_projects()
df_organizations = load_orgs()

# Display Min and Max Dates
min_date = projects['startDate'].min()
max_date = projects['endDate'].max()
st.write(f"**Min Start Date:** {min_date}")
st.write(f"**Max End Date:** {max_date}")

# --- Filters ---
st.sidebar.header("Filters")

# Date range filter
start_date = st.sidebar.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
end_date = st.sidebar.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)

# Cluster filter
clusters = projects['cluster'].unique().tolist()
selected_clusters = st.sidebar.multiselect("Select Clusters", options=clusters, default=clusters)

# Funding scheme filter
funding_schemes = projects['fundingScheme'].unique().tolist()
selected_funding_schemes = st.sidebar.multiselect("Select Funding Schemes", options=funding_schemes,
                                                  default=funding_schemes)

# # Keyword search
# search_keyword = st.sidebar.text_input("Search Title")

# Objective Keyword search
search_objective = st.sidebar.text_input("Search Objective")

# Apply filters
filtered_df = projects[(projects['startDate'] >= pd.to_datetime(start_date)) & (projects['endDate'] <= pd.to_datetime(end_date))]
filtered_df = filtered_df[filtered_df['cluster'].isin(selected_clusters)]
filtered_df = filtered_df[filtered_df['fundingScheme'].isin(selected_funding_schemes)]

# if search_keyword:
#     filtered_df = filtered_df[filtered_df['title'].str.contains(search_keyword, case=False, na=False)]

if search_objective:
    filtered_df = filtered_df[filtered_df['objective'].str.contains(search_objective, case=False, na=False)]

# Display filtered dataframe
st.write("### Filtered Data")
st.dataframe(filtered_df)

#Select project
selected_project = st.selectbox("Select a Project ID to View Organizations", filtered_df['id'].unique())
st.write('Results:'+str(filtered_df.shape[0]))
# st.write(filtered_df.shape[0])
if df_organizations is not None:
        st.write("### Participating Organizations")
        project_orgs = df_organizations[df_organizations['projectID'] == selected_project]
        st.dataframe(project_orgs)