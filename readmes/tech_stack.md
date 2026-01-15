# Tech Stack

This project is built with the following core technologies:

* **Language:** Python 3.10+
* **Web Framework:** [Streamlit](https://streamlit.io/) - For creating the interactive web dashboard.
* **Data Manipulation:** [Pandas](https://pandas.pydata.org/) - For reading, processing, and filtering the project data.
* **File Format:** CSV (`|` delimited) for processed data, XLSX for raw data.
* **User Preferences:** SQLite - A single-file, serverless database for storing user-specific data like watchlists and saved searches.
* **Logging:** [Loguru](https://loguru.readthedocs.io/en/stable/) - For simple and effective application logging.

## AI & Semantic Search

The application features a semantic search engine capable of understanding the *intent* behind a query, not just matching keywords.

* **Library:** [sentence-transformers](https://www.sbert.net/) (based on Hugging Face Transformers).
* **Model:** `all-MiniLM-L6-v2`.
  * **Why this choice?** This model offers the best trade-off between speed and performance. It maps sentences and paragraphs to a 384-dimensional dense vector space and is significantly faster than larger BERT-based models while maintaining high accuracy for semantic similarity tasks. This allows the search to run efficiently on standard CPUs without requiring GPU acceleration.
* **Mechanism:**
    1. **Vectorization:** We generate "embeddings" (vector representations) for every project by combining its Title, Objective, and Topics.
    2. **Cosine Similarity:** When a user searches, their query is converted into a vector. We calculate the cosine similarity between the query vector and all project vectors.
    3. **Ranking:** Projects are ranked by this similarity score (0 to 1), effectively surfacing the most *conceptually* relevant results even if they don't share exact words.
