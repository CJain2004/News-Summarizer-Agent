import trafilatura

def extract_content(url: str) -> str:
    """
    Extracts the main text content from a URL using Trafilatura.
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            text = trafilatura.extract(downloaded)
            if text and len(text) > 200:
                return text[:15000] # Limit size
        return ""
    except Exception as e:
        print(f"Error extracting {url}: {e}")
        return ""
