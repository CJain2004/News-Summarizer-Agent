# Financial News Aggregator

A real-time financial news aggregation system that collects, organizes, and summarizes news for major tech companies (Microsoft, Google, Apple, Meta).

## Features

- **Automated News Collection**: Fetches news via RSS feeds and scrapes full content.
- **Intelligent Deduplication**: Prevents duplicate stories using title normalization and content hashing.
- **AI-Powered Summaries**: Generates concise summaries using Groq API (Llama 3).
- **Auto-Cleanup**: Automatically removes news older than 7 days to keep the feed fresh.
- **Modern UI**: Clean, responsive React frontend with dark mode support.

## Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy, SQLite
- **Frontend**: React, Vite, Tailwind CSS
- **AI**: Groq API (Llama 3.1-8b)

## Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 18+
- Groq API Key

### Backend Setup

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```

2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Configure Environment:
    - Create a `.env` file in the `backend` directory.
    - Add your Groq API Key:
      ```env
      GROQ_API_KEY=your_api_key_here
      ```

5.  Run the server:
    ```bash
    uvicorn main:app --reload
    ```
    The API will run at `http://localhost:8000`.

### Frontend Setup

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```

2.  Install dependencies:
    ```bash
    npm install
    ```

3.  Run the development server:
    ```bash
    npm run dev
    ```
    The app will open at `http://localhost:5173`.

## Usage
1.  Open the frontend application.
2.  Click **"Sync News"** to trigger the background ingestion task.
3.  The system will fetch new articles, remove duplicates, and generate summaries.
4.  Use the filter buttons to view news for specific companies.
