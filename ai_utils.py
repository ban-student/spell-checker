"""
AI-based text enhancement using Google Gemini.
Needs a free API key from aistudio.google.com.
"""
from google import genai

_SYSTEM_PROMPT = (
    "You are a professional writing assistant. Improve the clarity, tone, "
    "and fluency of the text the user gives you WITHOUT changing its "
    "original meaning. Keep the same language as the input (English or "
    "Hindi). "
    "When you encounter a misspelled or ambiguous word, correct it to the "
    "most common, everyday word it most plausibly was intended to be -- "
    "based on keyboard/phonetic similarity and sentence context. Do NOT "
    "reinterpret it as an acronym, abbreviation, proper noun, or unusual "
    "term unless the surrounding sentence clearly calls for one. "
    "For example, in casual sentences about people or places, prefer common "
    "nouns like 'city' over uncommon readings like an acronym. "
    "Return only the improved text, with no preamble or explanation."
)


def enhance_text(text: str, api_key: str, model: str = "gemini-flash-latest") -> str:
    """
    Send `text` to a Gemini model and return an improved version.
    Raises ValueError if no API key is supplied.
    """
    if not api_key:
        raise ValueError("A Gemini API key is required for AI enhancement.")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=f"{_SYSTEM_PROMPT}\n\nText to improve:\n{text}",
    )
    return response.text.strip()
