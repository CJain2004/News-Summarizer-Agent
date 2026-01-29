import feedparser
import datetime
from typing import List, Dict
import re
import hashlib
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from difflib import SequenceMatcher

COMPANIES = {
    "Microsoft": "Microsoft",
    "Google": "Google",
    "Apple": "Apple",
    "Meta": "Meta"
}
def normalize_title(title: str) -> str:
    t = (title or "").strip()
    # remove trailing " - Source", " — Source", ": Source" common patterns
    t = re.sub(r'\s+[-–—:|]\s*[^-–—:|]{2,80}$', '', t)
    t = re.sub(r'\s+', ' ', t)                   # collapse whitespace
    t = re.sub(r'[^\w\s]', '', t)                # remove punctuation
    return t.lower()

def canonicalize_url(url: str) -> str:
    try:
        p = urlparse(url)
    except Exception:
        return url or ""
    qs = parse_qs(p.query, keep_blank_values=True)
    # remove common tracking params
    for k in list(qs.keys()):
        if k.startswith('utm_') or k in ('utm_source','utm_medium','utm_campaign','ref','fbclid','gclid'):
            qs.pop(k, None)
    # sort query params for determinism
    sorted_qs = urlencode(sorted((k, v[0]) for k, v in qs.items()))
    return urlunparse((p.scheme, p.netloc, p.path.rstrip('/'), p.params, sorted_qs, ''))

def compute_hash(text: str) -> str:
    return hashlib.sha256((text or "").encode('utf-8')).hexdigest()

def similar(a: str, b: str, thresh: float = 0.92) -> bool:
    return SequenceMatcher(None, a, b).ratio() >= thresh



# Bing News RSS URL
RSS_URL = "https://www.bing.com/news/search?q={query}&format=rss"

def fetch_rss_feed(company: str) -> List[Dict]:
    query = company
    url = RSS_URL.format(query=query)
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries:
        published_parsed = getattr(entry, 'published_parsed', None)
        pub_date = datetime.datetime(*published_parsed[:6]) if published_parsed else datetime.datetime.now()
        source = getattr(entry, 'source', None)
        source = source.title if source and hasattr(source, 'title') else "Unknown"

        title = entry.title
        url_raw = entry.link
        title_norm = normalize_title(title)
        url_norm = canonicalize_url(url_raw)

        articles.append({
            "title": title,
            "title_norm": title_norm,
            "url": url_raw,
            "url_norm": url_norm,
            "published_at": pub_date,
            "source": source,
            "company": company
        })
    return articles


def fetch_all_news() -> List[Dict]:
    all_articles = []
    seen_urls = set()
    seen_titles = []   # keep list to allow fuzzy checks

    for company in COMPANIES.keys():
        articles = fetch_rss_feed(company)
        for art in articles:
            if art['url_norm'] in seen_urls:
                continue
            # exact normalized-title check
            if art['title_norm'] in {t for t in [s for s in seen_titles]}:
                continue
            # fuzzy check against seen normalized titles
            skip = False
            for t in seen_titles:
                if similar(art['title_norm'], t, thresh=0.92):
                    skip = True
                    break
            if skip:
                continue

            seen_urls.add(art['url_norm'])
            seen_titles.append(art['title_norm'])
            all_articles.append(art)

    return all_articles

