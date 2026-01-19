# HopOn - Horizon Europe Project Finder

**HopOn** is a specialized Streamlit dashboard designed to identify "Hop-on" opportunities within Horizon Europe projects, which allow entities from Widening countries to join specific ongoing research consortiums.

## Architecture Overview

The application follows a simple, functional structure suitable for Streamlit development:

* `app.py`: The main entry point. Handles **Authentication** and routing.
* `components/`: Modular UI components (`sidebar.py`, `project_list.py`).
* `utils/`: Backend logic:
  * `data_loader.py`: Efficient Parquet/CSV hybrid data loading.
  * `db.py` & `models.py`: **SQLAlchemy ORM** layer for database interactions.
  * `ai.py`: Interface for GenAI features.
* `migrations/`: **Alembic** database migration scripts.
* `data/`:
  * `raw/` & `processed/`: Project data (CSV/Parquet).
  * `db/`: SQLite database (Development).

For more details, see:

* [**Tech Stack**](./readmes/tech_stack.md)
* [**Data Pipeline**](./readmes/pipeline.md)
* [**AI Engine & Intelligence**](./readmes/ai_engine.md) 🧠
* [**Performance & Optimization**](./readmes/performance.md) ⚡
* [**Security Architecture**](./readmes/security.md) 🛡️

## How to Run

### Prerequisites

* Python 3.10 or higher

### Installation

1. **Clone the repository and navigate into it.**
2. **Create and activate a virtual environment.**
3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Initialize Database:**
    The application uses Alembic for migrations. Run this to set up the database:

    ```bash
    alembic upgrade head
    ```

5. **Create an Admin User:**
    Since registration is Invite-Only, create your first user via CLI:

    ```bash
    python scripts/manage_users.py add <username> <password> --name "Your Name"
    ```

### Running the Dashboard

To start the web interface with integrated logging:

```bash
python run.py
```

**Credentials:** Log in with the username/password you created in step 5.
