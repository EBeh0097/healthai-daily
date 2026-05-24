from openai import OpenAI
from utils.secrets import get_secret

REGION_TONE_GUIDANCE = {
    "North America": "confident, concise, business-news style delivery",
    "Latin America": "warm, energetic, globally professional delivery",
    "Europe": "measured, analytical, policy-aware delivery",
    "Asia": "innovation-focused, precise, modern technology newsroom delivery",
    "Africa": "optimistic, dignified, innovation-centered delivery",
}

DEFAULT_TONE = "professional, factual, globally credible newsroom delivery"

def get_region_tone(region: str) -> str:
    return REGION_TONE_GUIDANCE.get(region, DEFAULT_TONE)

def write_shorts_script(
    story: dict,
    fact_check_notes: str,
    brand_name: str = "MedPulse AI Global"
) -> str:

    api_key = get_secret("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY was not found.")

    if not story.get("link"):
        return "No script generated because this story has no citation URL."

    client = OpenAI(api_key=api_key)

    region = story.get("region", "Global")
    tone_guidance = get_region_tone(region)

    prompt = f"""
You are an elite global healthcare AI news producer writing YouTube Shorts for {brand_name}.

IMPORTANT STYLE RULES:
- Sound like Bloomberg Tech, Reuters, CNBC Tech, or a professional AI newsroom.
- Start immediately with the news hook.
- Greeting/opening must be EXTREMELY short (0–3 words max) OR omitted entirely.
- No influencer language.
- No hype phrases.
- No fake excitement.
- No long intro.
- No clickbait.
- No exaggerated medical claims.
- No 'Hey guys welcome back'.
- Maximize information density in first 5 seconds.
- The story itself is the exciting part.
- Keep delivery globally intelligent and authoritative.
- Maintain strong audience retention pacing.
- Include why the story matters.
- Mention the source naturally.
- End with a thoughtful viewer question.

VOICE/TONE FOR THIS REGION:
{tone_guidance}

TARGET LENGTH:
35–50 seconds spoken naturally.

OUTPUT FORMAT EXACTLY:

Quick intro:
Hook:
Main story:
Why it matters:
Source line:
Viewer question:
Title options:
Hashtags:

STORY INFORMATION:
Region: {story.get("region")}
Title: {story.get("title")}
Source: {story.get("source")}
URL: {story.get("link")}
Date: {story.get("date")}
Snippet: {story.get("snippet")}

FACT CHECK NOTES:
{fact_check_notes}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.45,
    )

    return response.choices[0].message.content.strip()
