# HopOn - Horizon Europe Project Finder

## Overview

**HopOn** is a specialized dashboard designed for the DataLab team to identify "Hop-on" opportunities within Horizon Europe projects. 

The **Hop-on Facility** (Horizon Europe) allows legal entities from "Widening countries" (countries with lower Research & Innovation performance) to join ongoing Research and Innovation Actions (RIA) consortiums that currently have **no** partners from Widening countries.

This application automatically filters EU project data to find these exact opportunities.

## Key Features

*   **Eligibility Filtering:** Automatically filters for projects that:
    *   Start after Jan 1, 2024.
    *   End after Sept 25, 2027.
    *   **Crucially:** Currently have **ZERO** participants from Widening countries.
*   **Cluster Classification:** Automatically categorizes projects into Horizon Europe Clusters (Health, Digital, Climate, etc.) based on their topic ID.
*   **Interactive Dashboard:** A Streamlit interface to search, filter, and inspect potential projects and their current consortium members.

## Project Structure

*   `app.py`: The main Streamlit dashboard application.
*   `notebooks/data_viewer.ipynb`: Jupyter notebook that processes raw Excel data.
*   `data/`:
    *   `raw/`: Directory containing raw source data (Excel files) from EU CORDIS.
    *   `processed/`: Directory containing filtered CSV files used by the app.
*   `requirements.txt`: Python dependencies.
*   `updates_to_be_done.md`: Track future tasks.

## Setup & Installation

### Prerequisites
*   Python 3.10 or higher

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/idimitriadis/HopOn.git
    cd HopOn
    ```

2.  **Create a virtual environment:**
    ```bash
    # Windows
    python -m venv .venv
    .\.venv\Scripts\activate

    # macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the Dashboard
To start the web interface:

```bash
streamlit run app.py
```
The application will open in your default browser (usually at `http://localhost:8501`).

### Updating the Data
If you have new raw data (Excel files) in the `data/` directory, you can regenerate the filtered CSVs by running the notebook:

1.  Place updated `project.xlsx`, `organization.xlsx`, `topics.xlsx`, etc., in the `data/` folder.
2.  Run the notebook via Jupyter or command line:
    ```bash
    jupyter nbconvert --to python --execute data_viewer.ipynb
    ```
    *Or open `data_viewer.ipynb` in your preferred editor and Run All Cells.*

## Data Sources
The data is derived from the European Commission's CORDIS database.
*   **Widening Countries included in filter:** EL (Greece), BG (Bulgaria), HR (Croatia), CZ (Czechia), EE (Estonia), HU (Hungary), LV (Latvia), LT (Lithuania), MT (Malta), PL (Poland), PT (Portugal), RO (Romania), SK (Slovakia), SI (Slovenia), CY (Cyprus), and associated countries.