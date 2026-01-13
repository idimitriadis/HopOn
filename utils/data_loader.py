import pandas as pd
import streamlit as st
import os
from utils.logger import logger

@st.cache_data
def load_projects():
    file_path = 'data/processed/projects.csv'
    if not os.path.exists(file_path):
         logger.warning(f"Projects file not found at {file_path}")
         return pd.DataFrame()

    try:
        logger.info(f"Loading projects from {file_path}")
        projects = pd.read_csv(file_path, delimiter='|')
        projects['startDate'] = pd.to_datetime(projects['startDate'], errors='coerce')
        projects['endDate'] = pd.to_datetime(projects['endDate'], errors='coerce')
        
        # Clean totalCost: replace comma with dot and convert to numeric
        if 'totalCost' in projects.columns:
            projects['totalCost'] = projects['totalCost'].astype(str).str.replace(',', '.', regex=False)
            projects['totalCost'] = pd.to_numeric(projects['totalCost'], errors='coerce').fillna(0)

        projects['id'] = projects['id'].astype('str')
        projects = projects[['id','acronym','title','objective','cluster','topics','fundingScheme','startDate','endDate','legalBasis','grantDoi','totalCost']]
        logger.success(f"Loaded {len(projects)} projects.")
        return projects
    except Exception as e:
        logger.exception(f"Error loading projects: {e}")
        return pd.DataFrame()


@st.cache_data
def load_orgs():
    file_path = 'data/processed/orgs.csv'
    if not os.path.exists(file_path):
         logger.warning(f"Organizations file not found at {file_path}")
         return pd.DataFrame()

    try:
        logger.info(f"Loading organizations from {file_path}")
        orgs = pd.read_csv(file_path, delimiter='|')
        orgs['projectID'] = orgs['projectID'].astype('str')
        
        # Clean ecContribution
        if 'ecContribution' in orgs.columns:
            orgs['ecContribution'] = orgs['ecContribution'].astype(str).str.replace(',', '.', regex=False)
            orgs['ecContribution'] = pd.to_numeric(orgs['ecContribution'], errors='coerce').fillna(0)

        orgs = orgs[['name','activityType','city','country','role','organizationURL','projectID','order','ecContribution','contactForm']]
        logger.success(f"Loaded {len(orgs)} organizations.")
        return orgs
    except Exception as e:
        logger.exception(f"Error loading organizations: {e}")
        return pd.DataFrame()