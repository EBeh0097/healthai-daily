from urllib.parse import urlparse

def source_name_from_url(url: str) -> str:
    if not url:
        return "Unknown Source"
    try:
        domain = urlparse(url).netloc.replace("www.", "")
        return domain or "Unknown Source"
    except Exception:
        return "Unknown Source"

def has_valid_citation(story: dict) -> bool:
    return bool(story.get("link") or story.get("source_url"))

def normalize_story(raw: dict) -> dict:
    link = raw.get("link") or raw.get("source_url") or ""
    return {
        "title": raw.get("title", "").strip(),
        "link": link,
        "source": raw.get("source", "") or source_name_from_url(link),
        "date": raw.get("date", "") or raw.get("published_date", ""),
        "snippet": raw.get("snippet", "").strip(),
        "position": raw.get("position", None),
    }
