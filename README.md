# Financial News Aggregator

A real-time financial news aggregation system that collects, organizes, and summarizes news for major tech companies (Microsoft, Google, Apple, Meta). It is hosted live at: https://ai-finance-new-summarizer.streamlit.app/

## Features

- **Automated News Collection**: Fetches news via RSS feeds and scrapes full content.
- **Intelligent Deduplication**: Prevents duplicate stories using title normalization and content hashing.
- **AI-Powered Summaries**: Generates concise summaries using Groq API (Llama 3).
- **Auto-Cleanup**: Automatically removes news older than 7 days to keep the feed fresh.
- **Multiple Interfaces**: Run as a full-stack React app OR a simple Streamlit dashboard.

## Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy, SQLite
- **Frontend**: React, Vite, Tailwind CSS or Streamlit
- **AI**: Groq API (Llama 3.1-8b)

## Quick Start (Streamlit)
The easiest way to run the app is using **Streamlit**. This runs the scraper, database, and UI all in one command.

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Configure API Key**:
    The app supports **Hybrid Configuration** (works locally and in cloud):
    *   **Local**: Create a `.env` file in the root: `GROQ_API_KEY=gsk_...`
    *   **Streamlit Cloud**: Add to "Secrets" in the dashboard.
    *   **Local Streamlit (Optional)**: Create `.streamlit/secrets.toml`:
        ```toml
        GROQ_API_KEY = "gsk_..."
        ```
3.  **Run**:
    ```bash
    streamlit run streamlit_app.py
    ```

---

## Full Stack Setup (Advanced)
If you prefer the separate React Backend/Frontend architecture:

### Backend
1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  Navigate to `backend`: `cd backend`
3.  Run Server: `uvicorn main:app --reload` (Runs on port 8000)

### Frontend
1.  Navigate to `frontend`: `cd frontend`
2.  Install: `npm install`
3.  Run: `npm run dev` (Runs on port 5173)

## Usage
1.  Click **"Sync News"** to trigger ingestion.
2.  View the deduplicated news feed with AI summaries.
