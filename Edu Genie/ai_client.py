from functools import lru_cache

from google import genai
from google.genai import types

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
)


class GeminiConfigurationError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def get_client():

    if not GEMINI_API_KEY:

        raise GeminiConfigurationError(
            "GEMINI_API_KEY is not configured. "
            "Please add your Gemini API key to the .env file."
        )

    return genai.Client(
        api_key=GEMINI_API_KEY
    )


# ---------------------------------------------------------
# Normal text generation
# ---------------------------------------------------------

def generate_text(
    prompt: str,
    temperature: float = 0.4,
    max_output_tokens: int = 1200,
) -> str:

    client = get_client()

    response = client.models.generate_content(

        model=GEMINI_MODEL,

        contents=prompt,

        config=types.GenerateContentConfig(

            temperature=temperature,

            max_output_tokens=max_output_tokens,
        ),
    )

    text = getattr(
        response,
        "text",
        None
    )

    if not text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()


# ---------------------------------------------------------
# Structured JSON generation
# ---------------------------------------------------------

def generate_json(
    prompt: str,
    schema: dict,
    temperature: float = 0.2,
    max_output_tokens: int = 1800,
) -> str:

    client = get_client()

    response = client.models.generate_content(

        model=GEMINI_MODEL,

        contents=prompt,

        config=types.GenerateContentConfig(

            temperature=temperature,

            max_output_tokens=max_output_tokens,

            response_mime_type="application/json",

            response_schema=schema,
        ),
    )

    text = getattr(
        response,
        "text",
        None
    )

    if not text:

        raise RuntimeError(
            "Gemini returned an empty structured response."
        )

    return text.strip()