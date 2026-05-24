from urllib.parse import urlparse

def source_name_from_url(url: str) -> str:
    if not url:
        return "Unknown Source"
    try:
        domain = urlparse(url).netloc.replace("www.", "")
        return domain or "Unknown Source"
    except Exception:
        return "Unknown Source"

def stringify_source(source) -> str:
    if isinstance(source, dict):
        return source.get("name") or source.get("title") or source.get("source") or str(source)
    return str(source or "")

def normalize_story(raw: dict, region: str = "") -> dict:
    link = raw.get("link") or raw.get("source_url") or ""
    source = stringify_source(raw.get("source", "")) or source_name_from_url(link)
    return {
        "region": region,
        "title": str(raw.get("title", "")).strip(),
        "link": str(link).strip(),
        "source": source,
        "date": str(raw.get("date", "") or raw.get("published_date", "")).strip(),
        "snippet": str(raw.get("snippet", "")).strip(),
        "query": str(raw.get("query", "")).strip(),
    }

def has_valid_citation(story: dict) -> bool:
    return bool(story.get("link"))
