import streamlit as st

def render_project_list(filtered_df):
    st.write("### Filtered Data")
    st.dataframe(filtered_df, hide_index=True)

    # Select project
    if filtered_df.empty:
        return None
        
    selected_project = st.selectbox("Select a Project ID to View Organizations", filtered_df['id'].unique())
    st.write('Results: ' + str(filtered_df.shape[0]))
    
    return selected_project