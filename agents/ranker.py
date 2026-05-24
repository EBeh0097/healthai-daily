CREDIBLE_SOURCE_KEYWORDS = [
    "fda.gov", "nih.gov", "who.int", "nature.com", "nejm.org", "jamanetwork.com",
    "statnews.com", "fiercehealthcare.com", "beckershospitalreview.com",
    "healthcareitnews.com", "himss.org", "microsoft.com", "google",
    "nvidia.com", "epic.com", "nhs.uk", "ema.europa.eu",
]

TOPIC_KEYWORDS = [
    "ai", "artificial intelligence", "machine learning", "clinical", "healthcare",
    "hospital", "medical", "fda", "diagnostic", "patient", "ehr", "epic",
    "radiology", "llm", "digital health", "healthtech", "startup",
]

VIRAL_KEYWORDS = [
    "approved", "cleared", "launches", "partnership", "breakthrough",
    "study", "trial", "diagnosis", "cancer", "doctor", "hospital",
    "robot", "screening", "predict", "generative ai",
]

def score_story(story: dict) -> int:
    text = " ".join([
        str(story.get("title", "")),
        str(story.get("snippet", "")),
        str(story.get("source", "")),
        str(story.get("link", "")),
        str(story.get("region", "")),
    ]).lower()

    score = 0

    for kw in TOPIC_KEYWORDS:
        if kw in text:
            score += 2

    for kw in VIRAL_KEYWORDS:
        if kw in text:
            score += 3

    for src in CREDIBLE_SOURCE_KEYWORDS:
        if src in text:
            score += 6

    if story.get("link"):
        score += 5
    if story.get("date"):
        score += 2
    if story.get("error"):
        score -= 100

    return score

def rank_stories_by_region(stories: list[dict], top_per_region: int = 2) -> list[dict]:
    grouped = {}

    for story in stories:
        story = story.copy()
        story["score"] = score_story(story)
        region = story.get("region", "Unknown")
        grouped.setdefault(region, []).append(story)

    selected = []
    for region, region_stories in grouped.items():
        region_stories.sort(key=lambda x: x.get("score", 0), reverse=True)
        selected.extend(region_stories[:top_per_region])

    selected.sort(key=lambda x: (x.get("region", ""), -x.get("score", 0)))
    return selected
