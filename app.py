import streamlit as st
import pandas as pd
from utils.data_loader import load_projects, load_orgs
from components.sidebar import render_sidebar
from components.project_list import render_project_list

st.set_page_config(page_title="HopOn Projects", layout="wide")

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
if not df_organizations.empty:
    df_organizations = df_organizations[df_organizations['country'].isin(country_mapping.keys())]
    # Replace country codes with country names
    df_organizations['country'] = df_organizations['country'].map(country_mapping)

# Render Sidebar and get filters
filters = render_sidebar(projects)

# Apply filters
if not projects.empty and filters:
    filtered_df = projects[
        (projects['startDate'] >= pd.to_datetime(filters['start_date'])) &
        (projects['endDate'] <= pd.to_datetime(filters['end_date'])) &
        (projects['endDate'] > pd.to_datetime("2027-09-25"))  # Filter end date > 25th Sep 2027
        ]
    filtered_df = filtered_df[filtered_df['cluster'].isin(filters['selected_clusters'])]
    filtered_df = filtered_df[filtered_df['fundingScheme'].isin(filters['selected_funding_schemes'])]

    if filters['search_objective']:
        filtered_df = filtered_df[filtered_df['objective'].str.contains(filters['search_objective'], case=False, na=False)]
    if filters['search_id']:
        filtered_df = filtered_df[filtered_df['id'].str.contains(filters['search_id'], case=False, na=False)]
else:
    filtered_df = projects


# Create tabs
tab1, tab2 = st.tabs(["Projects", "Organisations"])

with tab1:
    st.header("Projects")
    
    if not projects.empty:
        min_date = projects['startDate'].min()
        max_date = projects['endDate'].max()
        st.write(f"**Min Start Date:** {min_date}")
        st.write(f"**Max End Date:** {max_date}")

    selected_project = render_project_list(filtered_df)

    # Detail View
    if filters and filters.get('search_id'):
        def format_row(row,df):
            return "\n\n".join(f"**{col}:** {row[col]}" for col in df.columns)

        # Convert entire DataFrame to formatted Markdown with line breaks
        formatted_text = "\n\n---\n\n".join(format_row(row,filtered_df) for _, row in filtered_df.iterrows())

        # Display formatted text using Markdown
        st.subheader("Info for specific project")
        st.markdown(formatted_text)

    # Org view for selected project
    if not df_organizations.empty and selected_project:
        st.write("### Participating Organizations")
        project_orgs = df_organizations[df_organizations['projectID'] == selected_project]
        project_orgs = project_orgs.sort_values(by=['order'],ascending=True)
        st.dataframe(project_orgs,hide_index=True)

with tab2:
    st.header("Organisations")
    
    if not df_organizations.empty:
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