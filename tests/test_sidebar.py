import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import date
from components.sidebar import render_sidebar

class TestSidebar(unittest.TestCase):

    @patch('components.sidebar.st')
    def test_render_sidebar(self, mock_st):
        # Setup mock data
        mock_projects = pd.DataFrame({
            'startDate': [pd.Timestamp('2024-01-01'), pd.Timestamp('2025-01-01')],
            'endDate': [pd.Timestamp('2026-01-01'), pd.Timestamp('2027-01-01')],
            'cluster': ['C1', 'C2'],
            'fundingScheme': ['F1', 'F2']
        })
        
        # Setup mock returns for sidebar widgets
        # Order in app.py: start_date, end_date, clusters, funding_schemes, project_id, objective
        mock_st.sidebar.date_input.side_effect = [date(2024, 1, 1), date(2027, 1, 1)] 
        mock_st.sidebar.multiselect.side_effect = [['C1'], ['F1']] 
        mock_st.sidebar.text_input.side_effect = ['123', 'keyword'] 

        # Call function
        filters = render_sidebar(mock_projects)

        # Assertions
        self.assertIsNotNone(filters)
        self.assertEqual(filters['start_date'], date(2024, 1, 1))
        self.assertEqual(filters['end_date'], date(2027, 1, 1))
        self.assertEqual(filters['selected_clusters'], ['C1'])
        self.assertEqual(filters['selected_funding_schemes'], ['F1'])
        self.assertEqual(filters['search_id'], '123')
        self.assertEqual(filters['search_objective'], 'keyword')
        
        # Verify widget calls
        self.assertTrue(mock_st.sidebar.header.called)

if __name__ == '__main__':
    unittest.main()
