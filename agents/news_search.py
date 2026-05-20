import requests
from utils.secrets import get_secret
from utils.citations import normalize_story, has_valid_citation

DEFAULT_QUERIES = [
    "AI in healthcare news",
    "FDA artificial intelligence medical device",
    "medical AI news",
    "Epic healthcare AI",
    "Google Health AI",
    "Microsoft healthcare AI",
    "NVIDIA healthcare AI",
    "healthcare AI startup",
]

def search_serpapi(query: str, num_results: int = 10) -> list[dict]:
    api_key = get_secret("SERPAPI_API_KEY")
    if not api_key:
        raise RuntimeError("SERPAPI_API_KEY was not found in environment, Streamlit secrets, or Google Secret Manager.")

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
            "position": item.get("position"),
        }
        story = normalize_story(raw)
        if story["title"] and has_valid_citation(story):
            story["query"] = query
            stories.append(story)

    return stories

def collect_news(queries: list[str] | None = None, max_per_query: int = 8) -> list[dict]:
    queries = queries or DEFAULT_QUERIES
    seen = set()
    all_stories = []

    for query in queries:
        try:
            results = search_serpapi(query, num_results=max_per_query)
            for story in results:
                key = story.get("link") or story.get("title")
                if key not in seen:
                    seen.add(key)
                    all_stories.append(story)
        except Exception as exc:
            all_stories.append({
                "title": f"Search failed for query: {query}",
                "link": "",
                "source": "System",
                "date": "",
                "snippet": str(exc),
                "query": query,
                "error": True,
            })

    return all_stories
