from openai import OpenAI
from utils.secrets import get_secret

def write_shorts_script(story: dict, fact_check_notes: str) -> str:
    api_key = get_secret("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY was not found.")

    if not story.get("link"):
        return "No script generated because this story has no citation URL."

    client = OpenAI(api_key=api_key)

    prompt = f'''
Create a 35-50 second YouTube Shorts script for an AI in healthcare channel.

Rules:
- Use only the facts provided.
- Do not exaggerate medical claims.
- Do not say "AI will replace doctors" unless directly supported.
- Include a cautious, credible tone.
- End with a viewer-friendly question.
- Include a source mention in plain language.

Story:
Title: {story.get("title")}
Source: {story.get("source")}
URL: {story.get("link")}
Date: {story.get("date")}
Snippet: {story.get("snippet")}

Fact-check notes:
{fact_check_notes}

Format:
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
