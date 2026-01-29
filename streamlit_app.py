import streamlit as st
import sys
import os
import time
import datetime
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import func

# Add backend to path to import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import database
import scraper
import extractor
import summarizer
import models

# Page Config
st.set_page_config(
    page_title="Financial News Agent",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize DB
database.init_db()

# --- CSS Styling ---
st.markdown("""
<style>
    .reportview-container {
        margin-top: -2em;
    }
    .stDeployButton {display:none;}
    .reportview-container .main .block-container{
        padding-top: 2rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.2rem;
    }
    /* Force text wrapping */
    .stAlert {
        word-wrap: break-word;
        word-break: break-word;
    }
</style>
""", unsafe_allow_html=True)

# --- Functions ---

def get_db():
    db = database.SessionLocal()
    try:
        return db
    finally:
        db.close()

def run_sync():
    """Run the ingestion pipeline (Scrape -> Dedup -> Summarize -> Save)"""
    db = database.SessionLocal()
    status_text = st.empty()
    progress_bar = st.progress(0)
    
    try:
        status_text.text("Starting cleanup...")
        # Cleanup old articles
        seven_days_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)
        db.query(database.Article).filter(
            database.Article.published_at < seven_days_ago
        ).delete()
        db.commit()
        
        status_text.text("Fetching RSS feeds...")
        articles_data = scraper.fetch_all_news()
        total = len(articles_data)
        progress_per_item = 1.0 / (total if total > 0 else 1)
        
        new_count = 0
        summary_engine = summarizer.Summarizer()

        for i, art in enumerate(articles_data):
            progress_bar.progress(min((i * progress_per_item), 0.9))
            
            # Fast dedup
            exists = db.query(database.Article).filter(
                (database.Article.url_norm == art["url_norm"]) |
                (database.Article.title_norm == art["title_norm"])
            ).first()

            if exists:
                continue

            status_text.text(f"Processing: {art['title'][:40]}...")
            
            content = extractor.extract_content(art["url"])
            if not content:
                continue

            content_hash = scraper.compute_hash(content)
            if db.query(database.Article).filter(database.Article.content_hash == content_hash).first():
                continue

            # Summarize
            summary = summary_engine.summarize(content)

            article = database.Article(
                title=art["title"],
                title_norm=art["title_norm"],
                url=art["url"],
                url_norm=art["url_norm"],
                published_at=art["published_at"],
                source=art["source"],
                company=art["company"],
                content=content,
                content_hash=content_hash,
                summary=summary
            )

            db.add(article)
            try:
                db.commit()
                new_count += 1
            except Exception:
                db.rollback()
            
            time.sleep(1) # Be gentle

        progress_bar.progress(1.0)
        return new_count
        
    finally:
        db.close()
        status_text.empty()
        progress_bar.empty()

# --- UI Layout ---

# Sidebar
with st.sidebar:
    st.title("Settings")
    
    # API Key Check
    if not os.environ.get("GROQ_API_KEY"):
        st.error("⚠️ GROQ_API_KEY missing! AI summaries will fail.")
        st.info("Go to App Settings > Secrets and add `GROQ_API_KEY`.")

    
    # Filter
    companies = ["All"] + list(scraper.COMPANIES.keys())
    selected_company = st.selectbox("Filter by Company", companies)
    
    st.divider()
    
    # Sync Button
    st.write("### Actions")
    if st.button("🔄 Sync News Now", type="primary", use_container_width=True):
        with st.spinner("Syncing news ecosystem..."):
            count = run_sync()
        if count > 0:
            st.success(f"Synced! Added {count} new articles.")
            time.sleep(2)
            st.rerun()
        else:
            st.info("No new articles found.")

# Main Content
st.title("📈 Financial News Summarizer")
st.caption("Real-time financial news with AI summaries")

# Get Data
db = get_db()
query = db.query(database.Article).order_by(database.Article.published_at.desc())

if selected_company != "All":
    query = query.filter(database.Article.company == selected_company)

articles = query.limit(50).all()
db.close()

if not articles:
    st.info("No articles found in database. Click 'Sync News Now' to start.")
else:
    # Grid Layout
    cols = st.columns(2) # 2 columns on medium screens
    
    for idx, art in enumerate(articles):
        with cols[idx % 2]:
            with st.container(border=True):
                # Header
                st.markdown(f"#### [{art.title}]({art.url})")
                
                # Metadata
                c1, c2 = st.columns([1, 1])
                c1.caption(f"📅 {art.published_at.strftime('%Y-%m-%d')}")
                c2.caption(f"🏢 {art.company}")
                
                # Summary with highlight (CSS handles word break)
                st.markdown(f"<div style='word-wrap: break-word;'>{art.summary}</div>", unsafe_allow_html=True)
                
                # Source - Removed as requested
    
    # Custom CSS for word breaking
    st.markdown("""
    <style>
        div[data-testid="stMarkdownContainer"] p {
            word-break: break-word;
        }
    </style>
    """, unsafe_allow_html=True)
