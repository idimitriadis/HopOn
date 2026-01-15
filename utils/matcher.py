import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
from utils.logger import logger
import streamlit as st

class ProjectMatcher:
    def __init__(self):
        # Load model efficiently
        # 'all-MiniLM-L6-v2' is fast and good for semantic search
        try:
            logger.info("Initializing Semantic Matcher (all-MiniLM-L6-v2)...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.embeddings = None
            self.project_ids = None
            logger.success("Semantic Matcher ready.")
        except Exception as e:
            logger.exception(f"Failed to load Semantic Model: {e}")
            self.model = None

    def encode_projects(self, df):
        """
        Generates embeddings for the projects dataframe.
        We combine 'title' + 'objective' + 'topics' for the fingerprint.
        """
        if self.model is None or df.empty:
            return

        logger.info(f"Encoding {len(df)} projects...")
        
        # Create a rich text representation for embedding
        # Title is heavily weighted (conceptually), Objective provides detail
        text_corpus = df.apply(lambda x: f"{x['title']} {x['objective']} {x['topics']}", axis=1).tolist()
        
        # Compute embeddings (returns numpy array)
        self.embeddings = self.model.encode(text_corpus, convert_to_tensor=True)
        self.project_ids = df['id'].tolist()
        
        logger.success("Project encoding complete.")

    def search(self, query, df, top_k=None):
        """
        Searches the projects for the query.
        Returns the DataFrame with a new 'Relevance' column, sorted.
        """
        if self.model is None or self.embeddings is None:
            logger.warning("Matcher not initialized or embeddings missing.")
            return df

        # Encode query
        query_embedding = self.model.encode(query, convert_to_tensor=True)

        # Compute Cosine Similarity
        # util.cos_sim returns a tensor of shape (1, num_projects)
        scores = util.cos_sim(query_embedding, self.embeddings)[0]

        # Convert to numpy and then to list
        scores_list = scores.cpu().numpy().tolist()

        # Add scores to the dataframe (we need to align by ID or Index)
        # Since we stored self.project_ids in order, and df hasn't changed order relative to our cache...
        # Wait, if df is filtered externally, we need to map scores by ID.
        
        score_map = dict(zip(self.project_ids, scores_list))
        
        # Create a copy to avoid SettingWithCopy warnings
        result_df = df.copy()
        
        # Map scores
        result_df['relevance_score'] = result_df['id'].map(score_map).fillna(0)
        
        # Sort
        result_df = result_df.sort_values('relevance_score', ascending=False)
        
        return result_df

    def get_similar_projects(self, project_id, df, top_k=5):
        """
        Finds projects similar to the given project_id based on embeddings.
        """
        if self.model is None or self.embeddings is None:
            return pd.DataFrame()

        # Find index of the project
        try:
            # We need the integer index in the embeddings tensor
            idx = self.project_ids.index(project_id)
        except ValueError:
            logger.warning(f"Project ID {project_id} not found in embeddings.")
            return pd.DataFrame()

        # Get embedding for this project
        target_embedding = self.embeddings[idx]

        # Compute cosine similarity against ALL projects
        scores = util.cos_sim(target_embedding, self.embeddings)[0]
        
        # Convert to list
        scores_list = scores.cpu().numpy().tolist()
        
        # Map to IDs
        score_map = dict(zip(self.project_ids, scores_list))
        
        # Create result DF
        result_df = df.copy()
        result_df['similarity_score'] = result_df['id'].map(score_map).fillna(0)
        
        # Sort desc
        result_df = result_df.sort_values('similarity_score', ascending=False)
        
        # Filter out the project itself (similarity is 1.0)
        result_df = result_df[result_df['id'] != project_id]
        
        return result_df.head(top_k)
