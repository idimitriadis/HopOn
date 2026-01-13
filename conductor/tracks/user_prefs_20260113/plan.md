# Implementation Plan - User Preferences

## Phase 1: Modular Refactoring [checkpoint: 0168f26]
- [x] Task: Create `utils/` and `components/` directories. 95bec1a
- [x] Task: Extract data loading logic to `utils/data_loader.py`. a2bafdc
    - [ ] Sub-task: Write Tests for data loader.
    - [ ] Sub-task: Implement `load_projects` and `load_orgs` in new module.
- [x] Task: Extract Sidebar/Filter logic to `components/sidebar.py`. e7579c2
    - [ ] Sub-task: Implement `render_sidebar` function that returns filter values.
- [x] Task: Extract Project List logic to `components/project_list.py`. e215eb7
    - [ ] Sub-task: Implement `render_project_list` taking dataframe as input.
- [x] Task: Update `app.py` to use the new modules. 20ecb50
    - [ ] Sub-task: Verify application functionality matches original.

## Phase 2: SQLite Backend Setup [checkpoint: 8d5f9fb]
- [x] Task: Create `utils/db.py` for database interactions. d6253d0
    - [x] Sub-task: Write Tests for DB connection and schema creation.
    - [x] Sub-task: Implement `init_db` to create `watchlist` and `saved_searches` tables.
    - [x] Sub-task: Implement helper functions: `add_to_watchlist`, `remove_from_watchlist`, `get_watchlist`.
    - [x] Sub-task: Implement helper functions: `save_search`, `get_saved_searches`, `delete_search`.

## Phase 3: Watchlist Implementation
- [x] Task: Integrate Watchlist UI in `components/project_list.py`. 3d1890d
    - [ ] Sub-task: Add "Star" column/button to the dataframe display or custom card layout.
    - [ ] Sub-task: Connect button click to `utils/db.py` functions.
- [x] Task: Add "Watchlist" Filter. 82aaa5c
    - [x] Sub-task: Update `components/sidebar.py` to include a "Show Favorites Only" toggle.
    - [x] Sub-task: Update filter logic to intersect with `get_watchlist()` IDs.

## Phase 4: Saved Search Implementation
- [ ] Task: Add "Save Search" UI to Sidebar.
    - [ ] Sub-task: Create text input for "Search Name" and "Save" button.
    - [ ] Sub-task: Serialize current filter state (JSON) and save to DB.
- [ ] Task: Add "Load Search" UI to Sidebar.
    - [ ] Sub-task: specific dropdown to select saved searches.
    - [ ] Sub-task: Logic to parse JSON and update session state widgets.
