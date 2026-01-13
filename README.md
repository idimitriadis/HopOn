# HopOn - Horizon Europe Project Finder

**HopOn** is a specialized Streamlit dashboard designed to identify "Hop-on" opportunities within Horizon Europe projects, which allow entities from Widening countries to join specific ongoing research consortiums.

## Architecture Overview

The application follows a simple, functional structure suitable for Streamlit development:

* `app.py`: The main entry point and user interface router.
* `components/`: Contains modular UI components (e.g., `sidebar.py`, `project_list.py`) that are imported into `app.py`.
* `utils/`: Contains backend logic and helper functions, such as `data_loader.py` for reading processed data and `db.py` for interacting with the user preferences database.
* `data/`:
  * `raw/`: Stores the original, unprocessed Excel files from CORDIS.
  * `processed/`: Contains the cleaned, filtered CSV files that the Streamlit app consumes.
  * `db/`: Holds the `user_prefs.db` SQLite database.
* `readmes/`: Contains detailed documentation on specific aspects of the project.

For more details, see:

* [**Tech Stack**](./readmes/tech_stack.md)
* [**Data Pipeline**](./readmes/pipeline.md)

## How to Run

### Prerequisites

* Python 3.10 or higher

### Installation

1. **Clone the repository and navigate into it.**
2. **Create and activate a virtual environment:**

    ```bash
    # Windows
    python -m venv .venv && .\.venv\Scripts\activate
    # macOS/Linux
    python3 -m venv .venv && source .venv/bin/activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Running the Dashboard

To start the web interface with integrated logging:

```bash
python run.py
```

This launcher will:
1. Start the Streamlit server in the background.
2. Stream logs directly to your terminal.
3. Handle safe shutdown (Ctrl+C).

The application will open in your default browser automatically.
