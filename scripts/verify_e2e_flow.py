from utils.db import create_user, get_user_id, delete_user, add_to_watchlist, get_watchlist, save_search, get_saved_searches, init_db
from utils.logger import setup_logger, logger
import streamlit as st
import json
import time

def run_e2e_test():
    """
    This script simulates a user interacting with the live application
    by performing operations on the same database. It should be run
    while the Streamlit server is active in the background.
    """
    # This setup ensures the script has its own configured logger
    # that points to the same file as the main app.
    st.session_state = {} 
    if 'logger_configured' not in st.session_state:
        setup_logger()
        st.session_state['logger_configured'] = True

    TEST_USER = "LiveE2EUser"
    TEST_PROJECT_ID = "101057404"
    TEST_SEARCH_NAME = "Live Test Search"
    
    logger.info("--- [E2E_SCRIPT] Starting Live E2E Test ---")

    # Ensure DB is initialized (harmless if already done)
    init_db()

    # 1. Create User
    user_id = create_user(TEST_USER)
    if user_id:
        logger.success(f"[E2E_SCRIPT] Step 1: User '{TEST_USER}' created with ID {user_id}.")
    else:
        # User might already exist from a previous failed run, try to get ID
        user_id = get_user_id(TEST_USER)
        if user_id:
             logger.warning(f"[E2E_SCRIPT] Step 1: User '{TEST_USER}' already existed. Proceeding with ID {user_id}.")
        else:
            logger.error("[E2E_SCRIPT] Step 1 FAILED: Could not create or find user.")
            return

    # 2. Add to Watchlist
    logger.info(f"[E2E_SCRIPT] Step 2: Adding project '{TEST_PROJECT_ID}' to watchlist for user {user_id}.")
    add_to_watchlist(TEST_PROJECT_ID, user_id)
    time.sleep(0.1) # Give server a moment to process
    watchlist = get_watchlist(user_id)
    if TEST_PROJECT_ID in watchlist:
        logger.success(f"[E2E_SCRIPT] Step 2 PASSED: Project confirmed in watchlist.")
    else:
        logger.error("[E2E_SCRIPT] Step 2 FAILED: Project not found in watchlist.")
        delete_user(user_id)
        return

    # 3. Save a search
    filters = {"start_date": "2026-01-01", "selected_clusters": ["Health"]}
    json_filters = json.dumps(filters)
    logger.info(f"[E2E_SCRIPT] Step 3: Saving search '{TEST_SEARCH_NAME}'.")
    save_search(TEST_SEARCH_NAME, json_filters, user_id)
    time.sleep(0.1)
    searches = get_saved_searches(user_id)
    if any(s['name'] == TEST_SEARCH_NAME for s in searches):
        logger.success(f"[E2E_SCRIPT] Step 3 PASSED: Saved search confirmed in database.")
    else:
        logger.error("[E2E_SCRIPT] Step 3 FAILED: Saved search not found.")
        delete_user(user_id)
        return

    logger.info("--- [E2E_SCRIPT] Script finished. Handing off for manual crash test. ---")
    logger.info("--- [E2E_SCRIPT] Please go to the browser and click the 'DEBUG_CRASH' button now. ---")


if __name__ == "__main__":
    run_e2e_test()

