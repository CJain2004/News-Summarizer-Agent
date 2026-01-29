from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    Text,
    Index,
    UniqueConstraint
)
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

DATABASE_URL = "sqlite:///./news_v2.db"

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)

    # Raw fields (what you show in UI)
    title = Column(String)
    url = Column(String)

    # Normalized / dedup fields
    title_norm = Column(String, index=True)
    url_norm = Column(String, index=True)
    content_hash = Column(String, unique=True, index=True)

    published_at = Column(DateTime, default=datetime.datetime.utcnow)
    source = Column(String)
    company = Column(String)

    summary = Column(Text)
    content = Column(Text)

    __table_args__ = (
        UniqueConstraint("url_norm", name="uq_url_norm"),
        Index("ix_title_norm_company", "title_norm", "company"),
    )

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
