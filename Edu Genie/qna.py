from ai_client import generate_text


SYSTEM_PROMPT = """
You are EduGenie, a helpful educational AI assistant.

Your job is to help students understand academic topics.

Rules:

1. Give accurate and useful answers.
2. Use simple language.
3. Keep answers reasonably concise.
4. Explain difficult terminology.
5. Give examples when helpful.
6. Do not invent sources.
7. If a question is ambiguous, mention the assumption briefly.
"""


def answer_question(question: str) -> str:

    prompt = f"""
{SYSTEM_PROMPT}

Student question:

{question}

Provide a clear answer suitable for a student.

If appropriate, include:
- explanation
- example
- important points
"""

    return generate_text(
        prompt,
        temperature=0.3,
        max_output_tokens=900,
    )