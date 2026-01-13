import streamlit as st
import pandas as pd
from utils.db import get_watchlist, add_to_watchlist, remove_from_watchlist

def render_project_list(filtered_df):
    st.write("### Filtered Data")
    
    if filtered_df.empty:
        st.write("No projects match the criteria.")
        return None
    
    # Get current watchlist
    watchlist = get_watchlist()
    
    # Add 'Favorite' column
    df_display = filtered_df.copy()
    df_display.insert(0, 'Favorite', df_display['id'].isin(watchlist))

    # Display editor
    edited_df = st.data_editor(
        df_display, 
        hide_index=True,
        column_config={
            "Favorite": st.column_config.CheckboxColumn(
                "Favorite",
                help="Select your favorite projects",
                default=False,
            )
        },
        disabled=[col for col in df_display.columns if col != 'Favorite'],
        key="project_editor"
    )

    # Detect Changes
    # Ensure indices align (they should if data_editor doesn't sort/filter internally independently)
    # Actually, data_editor returns the same dataframe structure.
    
    if not edited_df.equals(df_display):
        # New Favorites
        new_favs_mask = edited_df['Favorite'] & ~df_display['Favorite']
        new_fav_ids = edited_df.loc[new_favs_mask, 'id'].tolist()
        
        for pid in new_fav_ids:
            add_to_watchlist(pid)
            
        # Removed Favorites
        removed_favs_mask = ~edited_df['Favorite'] & df_display['Favorite']
        removed_fav_ids = edited_df.loc[removed_favs_mask, 'id'].tolist()
        
        for pid in removed_fav_ids:
            remove_from_watchlist(pid)
            
        # Force rerun to update UI immediately
        st.rerun()
    
    # Select project
    selected_project = st.selectbox("Select a Project ID to View Organizations", filtered_df['id'].unique())
    st.write('Results: ' + str(filtered_df.shape[0]))
    
    return selected_project
