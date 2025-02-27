import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="HopOn Projects", layout="wide")


@st.cache_data
def load_projects():
    projects = pd.read_csv('projects.csv', delimiter='|')
    projects['startDate'] = pd.to_datetime(projects['startDate'], errors='coerce')
    projects['endDate'] = pd.to_datetime(projects['endDate'], errors='coerce')
    projects['id'] = projects['id'].astype('str')
    projects = projects[['id','acronym','title','objective','cluster','topics','fundingScheme','startDate','endDate','legalBasis','grantDoi']]
    return projects


@st.cache_data
def load_orgs():
    orgs = pd.read_csv('orgs.csv', delimiter='|')
    orgs['projectID'] = orgs['projectID'].astype('str')
    orgs = orgs[['name','activityType','city','country','role','organizationURL','projectID','order','ecContribution','contactForm']]
    return orgs


# Dictionary mapping country codes to country names
country_mapping = {
    'IT': 'Italy', 'AT': 'Austria', 'CZ': 'Czech Republic', 'ES': 'Spain', 'FR': 'France', 'DE': 'Germany',
    'NL': 'Netherlands',
    'UK': 'United Kingdom', 'BE': 'Belgium', 'EE': 'Estonia', 'PL': 'Poland', 'HR': 'Croatia', 'IE': 'Ireland',
    'FI': 'Finland',
    'NO': 'Norway', 'LU': 'Luxembourg', 'DK': 'Denmark', 'CH': 'Switzerland', 'SE': 'Sweden', 'PT': 'Portugal',
    'RO': 'Romania',
    'BG': 'Bulgaria', 'LV': 'Latvia', 'SI': 'Slovenia', 'LT': 'Lithuania', 'SK': 'Slovakia', 'UA': 'Ukraine',
    'RS': 'Serbia',
    'CY': 'Cyprus', 'HU': 'Hungary', 'MT': 'Malta', 'MK': 'North Macedonia', 'IS': 'Iceland',
    'BA': 'Bosnia and Herzegovina',
    'AL': 'Albania', 'MD': 'Moldova', 'XK': 'Kosovo', 'ME': 'Montenegro'
}

# Title
st.title("Available Hopon Projects")
projects = load_projects()
df_organizations = load_orgs()

# Filter organizations to keep only those in Europe
df_organizations = df_organizations[df_organizations['country'].isin(country_mapping.keys())]

# Replace country codes with country names
df_organizations['country'] = df_organizations['country'].map(country_mapping)

# Create tabs
tab1, tab2 = st.tabs(["Projects", "Organisations"])

with tab1:
    st.header("Projects")
    # Display Min and Max Dates
    min_date = projects['startDate'].min()
    max_date = projects['endDate'].max()
    st.write(f"**Min Start Date:** {min_date}")
    st.write(f"**Max End Date:** {max_date}")

    # --- Filters ---
    st.sidebar.header("Project Filters")

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
    search_project_id = st.sidebar.text_input("Project ID")
    # Objective Keyword search
    search_objective = st.sidebar.text_input("Search Objective")

    # Apply filters
    filtered_df = projects[
        (projects['startDate'] >= pd.to_datetime(start_date)) & (projects['endDate'] <= pd.to_datetime(end_date))]
    filtered_df = filtered_df[filtered_df['cluster'].isin(selected_clusters)]
    filtered_df = filtered_df[filtered_df['fundingScheme'].isin(selected_funding_schemes)]

    if search_objective:
        filtered_df = filtered_df[filtered_df['objective'].str.contains(search_objective, case=False, na=False)]
    if search_project_id:
        filtered_df = filtered_df[filtered_df['id'].str.contains(search_project_id, case=False, na=False)]

    # Display filtered dataframe
    st.write("### Filtered Data")
    st.dataframe(filtered_df)

    # Select project
    selected_project = st.selectbox("Select a Project ID to View Organizations", filtered_df['id'].unique())
    st.write('Results: ' + str(filtered_df.shape[0]))

    if df_organizations is not None:
        st.write("### Participating Organizations")
        project_orgs = df_organizations[df_organizations['projectID'] == selected_project]
        st.dataframe(project_orgs)

with tab2:
    st.header("Organisations")

    # Organisation-specific filters
    org_countries = df_organizations['country'].unique().tolist()
    selected_countries = st.multiselect("Select Countries", options=org_countries, default=org_countries)

    org_types = df_organizations['activityType'].unique().tolist()
    selected_types = st.multiselect("Select Organisation Types", options=org_types, default=org_types)
    org_roles = df_organizations['role'].unique().tolist()
    selected_roles = st.multiselect("Select Organisation Role",options=org_roles,default='coordinator')
    # Organization name search
    search_org_name = st.text_input("Search Organisation Name")

    # Apply filters
    filtered_orgs = df_organizations[df_organizations['country'].isin(selected_countries)]
    filtered_orgs = filtered_orgs[filtered_orgs['activityType'].isin(selected_types)]
    filtered_orgs  = filtered_orgs[filtered_orgs['role'].isin(selected_roles)]

    if search_org_name:
        filtered_orgs = filtered_orgs[filtered_orgs['name'].str.contains(search_org_name, case=False, na=False)]

    # Display filtered organisations
    st.write("### Filtered Organisations")
    st.dataframe(filtered_orgs)
