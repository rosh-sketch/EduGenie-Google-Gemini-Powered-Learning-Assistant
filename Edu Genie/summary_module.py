from ai_client import generate_text


def summarize_text(text: str) -> str:

    prompt = f"""
Summarize the following educational passage.

The summary should:

- retain important facts
- retain definitions
- retain important relationships
- retain conclusions
- remove unnecessary repetition
- be easy for a student to revise

Use:

Heading

- Key point
- Key point
- Key point

Educational passage:

{text}
"""

    return generate_text(
        prompt,
        temperature=0.25,
        max_output_tokens=1000,
    )