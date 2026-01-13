import unittest
import sqlite3
import os
from utils.db import init_db, add_to_watchlist, remove_from_watchlist, get_watchlist, save_search, get_saved_searches, delete_search

class TestDB(unittest.TestCase):

    def setUp(self):
        # Use file DB for testing to persist across calls
        self.db_path = 'test_user_prefs.db'
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        init_db(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_watchlist_flow(self):
        # Test Add
        add_to_watchlist('proj_1', self.db_path)
        watchlist = get_watchlist(self.db_path)
        self.assertIn('proj_1', watchlist)
        
        # Test Duplicate Add (should ignore)
        add_to_watchlist('proj_1', self.db_path)
        watchlist = get_watchlist(self.db_path)
        self.assertEqual(len(watchlist), 1)

        # Test Remove
        remove_from_watchlist('proj_1', self.db_path)
        watchlist = get_watchlist(self.db_path)
        self.assertNotIn('proj_1', watchlist)

    def test_saved_search_flow(self):
        # Test Save
        filters = '{"cluster": "Health"}'
        save_search('My Search', filters, self.db_path)
        
        searches = get_saved_searches(self.db_path)
        self.assertEqual(len(searches), 1)
        self.assertEqual(searches[0]['name'], 'My Search')
        self.assertEqual(searches[0]['filters'], filters)
        
        # Test Delete
        search_id = searches[0]['id']
        delete_search(search_id, self.db_path)
        
        searches = get_saved_searches(self.db_path)
        self.assertEqual(len(searches), 0)

if __name__ == '__main__':
    unittest.main()