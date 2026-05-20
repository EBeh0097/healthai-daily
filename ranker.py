CREDIBLE_SOURCE_KEYWORDS = [
    "fda.gov",
    "nih.gov",
    "who.int",
    "nature.com",
    "nejm.org",
    "jamanetwork.com",
    "statnews.com",
    "fiercehealthcare.com",
    "beckershospitalreview.com",
    "healthcareitnews.com",
    "himss.org",
    "microsoft.com",
    "google",
    "nvidia.com",
    "epic.com",
]

TOPIC_KEYWORDS = [
    "ai",
    "artificial intelligence",
    "machine learning",
    "clinical",
    "healthcare",
    "hospital",
    "medical",
    "fda",
    "diagnostic",
    "patient",
    "ehr",
    "epic",
    "radiology",
    "llm",
]

def score_story(story: dict) -> int:
    text = " ".join([
        story.get("title", ""),
        story.get("snippet", ""),
        story.get("source", ""),
        story.get("link", ""),
    ]).lower()

    score = 0

    for kw in TOPIC_KEYWORDS:
        if kw in text:
            score += 2

    for src in CREDIBLE_SOURCE_KEYWORDS:
        if src in text:
            score += 5

    if story.get("link"):
        score += 3

    if story.get("date"):
        score += 2

    if any(word in text for word in ["breakthrough", "cleared", "approved", "launches", "partnership", "study", "trial"]):
        score += 2

    if story.get("error"):
        score -= 100

    return score

def rank_stories(stories: list[dict], top_n: int = 10) -> list[dict]:
    ranked = []
    for story in stories:
        story = story.copy()
        story["score"] = score_story(story)
        ranked.append(story)

    ranked.sort(key=lambda x: x.get("score", 0), reverse=True)
    return ranked[:top_n]
