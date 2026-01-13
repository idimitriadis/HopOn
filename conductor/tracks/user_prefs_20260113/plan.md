# Implementation Plan - User Preferences

## Phase 1: Modular Refactoring
- [x] Task: Create `utils/` and `components/` directories. 95bec1a
- [ ] Task: Extract data loading logic to `utils/data_loader.py`.
    - [ ] Sub-task: Write Tests for data loader.
    - [ ] Sub-task: Implement `load_projects` and `load_orgs` in new module.
- [ ] Task: Extract Sidebar/Filter logic to `components/sidebar.py`.
    - [ ] Sub-task: Implement `render_sidebar` function that returns filter values.
- [ ] Task: Extract Project List logic to `components/project_list.py`.
    - [ ] Sub-task: Implement `render_project_list` taking dataframe as input.
- [ ] Task: Update `app.py` to use the new modules.
    - [ ] Sub-task: Verify application functionality matches original.

## Phase 2: SQLite Backend Setup
- [ ] Task: Create `utils/db.py` for database interactions.
    - [ ] Sub-task: Write Tests for DB connection and schema creation.
    - [ ] Sub-task: Implement `init_db` to create `watchlist` and `saved_searches` tables.
    - [ ] Sub-task: Implement helper functions: `add_to_watchlist`, `remove_from_watchlist`, `get_watchlist`.
    - [ ] Sub-task: Implement helper functions: `save_search`, `get_saved_searches`, `delete_search`.

## Phase 3: Watchlist Implementation
- [ ] Task: Integrate Watchlist UI in `components/project_list.py`.
    - [ ] Sub-task: Add "Star" column/button to the dataframe display or custom card layout.
    - [ ] Sub-task: Connect button click to `utils/db.py` functions.
- [ ] Task: Add "Watchlist" Filter.
    - [ ] Sub-task: Update `components/sidebar.py` to include a "Show Favorites Only" toggle.
    - [ ] Sub-task: Update filter logic to intersect with `get_watchlist()` IDs.

## Phase 4: Saved Search Implementation
- [ ] Task: Add "Save Search" UI to Sidebar.
    - [ ] Sub-task: Create text input for "Search Name" and "Save" button.
    - [ ] Sub-task: Serialize current filter state (JSON) and save to DB.
- [ ] Task: Add "Load Search" UI to Sidebar.
    - [ ] Sub-task: specific dropdown to select saved searches.
    - [ ] Sub-task: Logic to parse JSON and update session state widgets.
