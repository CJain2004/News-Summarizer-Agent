from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ArticleBase(BaseModel):
    title: str
    url: str
    published_at: Optional[datetime]
    source: Optional[str] = None
    company: str
    summary: Optional[str] = None

class ArticleCreate(ArticleBase):
    content: Optional[str] = None

class Article(ArticleBase):
    id: int
    
    class Config:
        from_attributes = True
