from openai import OpenAI
from utils.secrets import get_secret

def fact_check_story(story: dict) -> dict:
    api_key = get_secret("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY was not found.")

    if not story.get("link"):
        return {
            "confidence": "Rejected",
            "fact_check_notes": "Rejected because no source URL was available.",
        }

    client = OpenAI(api_key=api_key)

    prompt = f'''
You are a careful healthcare AI newsroom editor.

Evaluate this story for factual reporting. Do not invent facts beyond the provided text.

Title: {story.get("title")}
Source: {story.get("source")}
URL: {story.get("link")}
Date: {story.get("date")}
Snippet: {story.get("snippet")}

Return:
1. Confidence: High, Medium, Low, or Reject
2. Main verified claim
3. What should NOT be overstated
4. Whether this is safe to turn into a YouTube Short
5. One-sentence reason
'''

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return {
        "confidence": "Review Required",
        "fact_check_notes": response.choices[0].message.content.strip(),
    }
