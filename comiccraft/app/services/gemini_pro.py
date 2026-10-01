from google import genai
from app.config import get_settings


def generate_story(
    story_prompt,
    character_name,
    setting,
    tone,
    art_style
):
    s = get_settings()

    if not s.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to your .env file."
        )

    prompt = f"""
Create a very short comic story.

Story idea: {story_prompt}
Character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}

Write exactly TWO lines.
Each line must be a complete sentence.
Return ONLY the two story lines.
"""

    # Create a fresh Gemini client for this request
    client = genai.Client(api_key=s.gemini_api_key)

    response = client.models.generate_content(
        model=s.gemini_story_model,
        contents=prompt,
    )

    story = response.text.strip()

    lines = [
        line.strip()
        for line in story.splitlines()
        if line.strip()
    ]

    if len(lines) >= 2:
        return "\n".join(lines[:2])

    return story