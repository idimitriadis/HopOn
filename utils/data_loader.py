import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_projects():
    if not os.path.exists('data/processed/projects.csv'):
         return pd.DataFrame()

    projects = pd.read_csv('data/processed/projects.csv', delimiter='|')
    projects['startDate'] = pd.to_datetime(projects['startDate'], errors='coerce')
    projects['endDate'] = pd.to_datetime(projects['endDate'], errors='coerce')
    projects['id'] = projects['id'].astype('str')
    projects = projects[['id','acronym','title','objective','cluster','topics','fundingScheme','startDate','endDate','legalBasis','grantDoi']]
    return projects


@st.cache_data
def load_orgs():
    if not os.path.exists('data/processed/orgs.csv'):
         return pd.DataFrame()

    orgs = pd.read_csv('data/processed/orgs.csv', delimiter='|')
    orgs['projectID'] = orgs['projectID'].astype('str')
    orgs = orgs[['name','activityType','city','country','role','organizationURL','projectID','order','ecContribution','contactForm']]
    return orgs