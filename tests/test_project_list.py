import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from components.project_list import render_project_list

class TestProjectList(unittest.TestCase):

    @patch('components.project_list.st')
    def test_render_project_list(self, mock_st):
        # Mock data
        mock_projects = pd.DataFrame({
            'id': ['1', '2'],
            'title': ['A', 'B']
        })
        
        # Mock widget returns
        mock_st.selectbox.return_value = '1'

        # Call function
        selected_id = render_project_list(mock_projects)

        # Assertions
        self.assertEqual(selected_id, '1')
        
        # Verify calls
        mock_st.write.assert_any_call("### Filtered Data")
        mock_st.dataframe.assert_called()
        mock_st.selectbox.assert_called()

if __name__ == '__main__':
    unittest.main()
