import requests
from utils.secrets import get_secret
from utils.citations import normalize_story, has_valid_citation
from agents.regional.config import REGIONAL_SEARCH_CONFIG

def search_serpapi(query: str, region: str, num_results: int = 10) -> list[dict]:
    api_key = get_secret("SERPAPI_API_KEY")
    if not api_key:
        raise RuntimeError("SERPAPI_API_KEY was not found.")

    params = {
        "engine": "google_news",
        "q": query,
        "api_key": api_key,
        "num": num_results,
        "hl": "en",
        "gl": "us",
    }

    response = requests.get("https://serpapi.com/search.json", params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    stories = []
    for item in data.get("news_results", []):
        raw = {
            "title": item.get("title", ""),
            "link": item.get("link", ""),
            "source": item.get("source", ""),
            "date": item.get("date", ""),
            "snippet": item.get("snippet", ""),
            "query": query,
        }
        story = normalize_story(raw, region=region)
        if story["title"] and has_valid_citation(story):
            stories.append(story)

    return stories

def collect_regional_news(regions: list[str] | None = None, max_per_query: int = 6) -> list[dict]:
    regions = regions or list(REGIONAL_SEARCH_CONFIG.keys())
    seen = set()
    all_stories = []

    for region in regions:
        queries = REGIONAL_SEARCH_CONFIG.get(region, [])
        for query in queries:
            try:
                results = search_serpapi(query=query, region=region, num_results=max_per_query)
                for story in results:
                    key = story.get("link") or f"{story.get('region')}::{story.get('title')}"
                    if key not in seen:
                        seen.add(key)
                        all_stories.append(story)
            except Exception as exc:
                all_stories.append({
                    "region": region,
                    "title": f"Search failed for query: {query}",
                    "link": "",
                    "source": "System",
                    "date": "",
                    "snippet": str(exc),
                    "query": query,
                    "error": True,
                })

    return all_stories
