from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
import time
import datetime

import database
import scraper
import extractor
import summarizer

database.init_db()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

summary_engine = summarizer.Summarizer()

def ingest_articles_task(db: Session):
    print("Starting ingestion task...")

    seven_days_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    db.query(database.Article).filter(
        database.Article.published_at < seven_days_ago
    ).delete()
    db.commit()

    articles_data = scraper.fetch_all_news()
    new_count = 0

    for art in articles_data:
        # Fast dedup before extraction
        exists = db.query(database.Article).filter(
            (database.Article.url_norm == art["url_norm"]) |
            (database.Article.title_norm == art["title_norm"])
        ).first()

        if exists:
            continue

        print(f"Processing: {art['title']}")
        time.sleep(2)

        content = extractor.extract_content(art["url"])
        if not content:
            continue

        content_hash = scraper.compute_hash(content)

        if db.query(database.Article).filter(
            database.Article.content_hash == content_hash
        ).first():
            continue

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
            summary=summary_engine.summarize(content)
        )

        db.add(article)
        try:
            db.commit()
            new_count += 1
        except Exception as e:
            db.rollback()
            print("Duplicate rejected by DB:", e)

    print(f"Ingestion complete. Added {new_count} new articles.")

@app.post("/ingest")
def trigger_ingestion(
    background_tasks: BackgroundTasks,
    db: Session = Depends(database.get_db)
):
    background_tasks.add_task(ingest_articles_task, db)
    return {"message": "Ingestion started"}

@app.get("/articles")
def get_articles(
    company: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(database.get_db)
):
    q = db.query(database.Article).order_by(
        database.Article.published_at.desc()
    )

    if company:
        q = q.filter(database.Article.company.contains(company))

    return q.limit(limit).all()
