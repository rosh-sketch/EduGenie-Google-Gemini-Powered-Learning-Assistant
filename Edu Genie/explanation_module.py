from ai_client import generate_text

from config import (
    USE_LOCAL_EXPLAINER,
    LOCAL_EXPLAINER_MODEL,
)


# ---------------------------------------------------------
# Optional local LaMini model
# ---------------------------------------------------------

def _local_explain(topic: str) -> str:

    from transformers import pipeline

    generator = pipeline(
        "text2text-generation",
        model=LOCAL_EXPLAINER_MODEL,
    )

    prompt = f"""
Explain the following educational topic
to a complete beginner.

Use:
- simple language
- short sentences
- one example
- important points

Topic:

{topic}
"""

    result = generator(
        prompt,
        max_new_tokens=180,
        do_sample=False,
    )

    return result[0]["generated_text"].strip()


# ---------------------------------------------------------
# Main explanation function
# ---------------------------------------------------------

def explain_topic(topic: str) -> str:

    # Try local LaMini model if enabled
    if USE_LOCAL_EXPLAINER:

        try:

            return _local_explain(topic)

        except Exception:

            # Fall back to Gemini
            pass


    # Gemini fallback/default
    prompt = f"""
Explain the following concept to a beginner.

Topic:

{topic}

Requirements:

- Use plain language.
- Assume the learner has little prior knowledge.
- Give a simple analogy or example.
- Avoid unnecessary jargon.
- Finish with 2 or 3 key takeaways.
"""

    return generate_text(
        prompt,
        temperature=0.35,
        max_output_tokens=900,
    )