from utils.db import create_user, get_user_id, delete_user, add_to_watchlist, get_watchlist
from utils.logger import setup_logger, logger
import streamlit as st
import time

def run_live_test():
    # Setup logger just for this script's context
    st.session_state = {}
    if 'logger_configured' not in st.session_state:
        setup_logger()
        st.session_state['logger_configured'] = True

    TEST_USER = "LiveE2EUser"
    TEST_PROJECT_ID = "101057404"
    
    logger.info("--- Starting LIVE E2E Test ---")

    # 1. Create User
    user_id = create_user(TEST_USER)
    if user_id:
        logger.success(f"Step 1: User '{TEST_USER}' created with ID {user_id}.")
    else:
        logger.error("Step 1 FAILED: Could not create user.")
        return

    # 2. Add to Watchlist
    add_to_watchlist(TEST_PROJECT_ID, user_id)
    watchlist = get_watchlist(user_id)
    if TEST_PROJECT_ID in watchlist:
        logger.success(f"Step 2: Project '{TEST_PROJECT_ID}' added to user's watchlist.")
    else:
        logger.error("Step 2 FAILED: Project not found in watchlist.")
        delete_user(user_id)
        return

    logger.info("Live test actions successful. Now attempting to simulate a crash.")
    # In a real scenario, this would be an HTTP request to a specific endpoint.
    # Here, we'll just log that we would be crashing the app now.
    logger.warning("SIMULATING CRASH: A real test would now send a request to the crash endpoint.")

    # Clean up the user
    delete_user(user_id)
    logger.success(f"Step 3: Cleaned up user '{TEST_USER}'.")

    logger.info("--- LIVE E2E Test Script Finished ---")


if __name__ == "__main__":
    run_live_test()
