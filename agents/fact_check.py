from openai import OpenAI
from utils.secrets import get_secret

def fact_check_story(story: dict) -> dict:
    api_key = get_secret("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY was not found.")

    if not story.get("link"):
        return {
            "confidence": "Rejected",
            "claim_risk": "High",
            "fact_check_notes": "Rejected because no source URL was available.",
        }

    client = OpenAI(api_key=api_key)

    prompt = f'''
You are a careful healthcare AI newsroom editor for MedPulse AI Global.

Evaluate this story for factual reporting. Do not invent facts beyond the provided text.

Region: {story.get("region")}
Title: {story.get("title")}
Source: {story.get("source")}
URL: {story.get("link")}
Date: {story.get("date")}
Snippet: {story.get("snippet")}

Return exactly these sections:
Confidence: High / Medium / Low / Reject
Medical claim risk: Low / Medium / High
Main verified claim:
What not to overstate:
Safe for Shorts: Yes / No
Reason:
'''

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    notes = response.choices[0].message.content.strip()
    confidence = "Review Required"
    claim_risk = "Review Required"

    for line in notes.splitlines():
        if line.lower().startswith("confidence:"):
            confidence = line.split(":", 1)[1].strip()
        if line.lower().startswith("medical claim risk:"):
            claim_risk = line.split(":", 1)[1].strip()

    return {
        "confidence": confidence,
        "claim_risk": claim_risk,
        "fact_check_notes": notes,
    }
