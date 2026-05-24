from openai import OpenAI
from utils.secrets import get_secret

def write_shorts_script(story: dict, fact_check_notes: str, brand_name: str = "MedPulse AI Global") -> str:
    api_key = get_secret("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY was not found.")

    if not story.get("link"):
        return "No script generated because this story has no citation URL."

    client = OpenAI(api_key=api_key)

    prompt = f'''
Create a 35-50 second YouTube Shorts script for {brand_name}.

Rules:
- Use only the facts provided.
- Do not exaggerate clinical or medical claims.
- Do not imply diagnosis/treatment effectiveness unless stated in the source.
- Keep the tone factual, attractive, and globally relevant.
- Mention the region.
- Include source attribution in plain language.
- End with a viewer-friendly question.

Story:
Region: {story.get("region")}
Title: {story.get("title")}
Source: {story.get("source")}
URL: {story.get("link")}
Date: {story.get("date")}
Snippet: {story.get("snippet")}

Fact-check notes:
{fact_check_notes}

Format exactly:
Hook:
Script:
Source line:
Title options:
Hashtags:
'''

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    return response.choices[0].message.content.strip()
