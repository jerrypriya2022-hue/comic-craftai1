from app.config import get_settings
from app.models import PanelOutline

_CLIENT = None


def _client():
    global _CLIENT

    if _CLIENT is not None:
        return _CLIENT

    from google import genai

    s = get_settings()

    if not s.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to your .env file."
        )

    _CLIENT = genai.Client(
        api_key=s.gemini_api_key
    )

    return _CLIENT


def generate_outline(
    story_prompt,
    character_name,
    setting,
    tone,
    art_style
):
    s = get_settings()

    prompt = f"""
Create a coherent 5-panel comic outline.

Story idea: {story_prompt}

Main character: {character_name}

Setting: {setting}

Tone: {tone}

Art style: {art_style}

Requirements:
Exactly 5 panels.
Preserve character and visual continuity.
Each panel needs:
- title
- scene_description
- detailed image_prompt

Clear beginning, development, climax and ending.
No text or speech bubbles inside images.
"""

    from google.genai import types

    client = _client()

    response = client.models.generate_content(
        model=s.gemini_outline_model,
        contents=prompt,
    
config=types.GenerateContentConfig(
    response_mime_type="application/json",
    response_schema=list[PanelOutline],
),

    )

    if response.parsed:
        return [
            x.model_dump()
            for x in response.parsed
        ][:5]

    import json

    return json.loads(response.text)[:5]