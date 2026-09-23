import json

from ai_client import generate_json

from schemas import QuizResult


# ---------------------------------------------------------
# Gemini JSON schema
# ---------------------------------------------------------

QUIZ_SCHEMA = {

    "type": "object",

    "properties": {

        "questions": {

            "type": "array",

            "minItems": 3,

            "maxItems": 3,

            "items": {

                "type": "object",

                "properties": {

                    "question": {
                        "type": "string"
                    },

                    "options": {

                        "type": "array",

                        "minItems": 4,

                        "maxItems": 4,

                        "items": {
                            "type": "string"
                        },
                    },

                    "correct_answer": {
                        "type": "string"
                    },

                    "explanation": {
                        "type": "string"
                    },
                },

                "required": [
                    "question",
                    "options",
                    "correct_answer",
                    "explanation",
                ],
            },
        }
    },

    "required": [
        "questions"
    ],
}


# ---------------------------------------------------------
# Clean markdown code blocks
# ---------------------------------------------------------

def clean_json_block(raw: str) -> str:

    text = raw.strip()

    if text.startswith("```"):

        lines = text.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    return text


# ---------------------------------------------------------
# Generate quiz
# ---------------------------------------------------------

def generate_quiz(passage: str) -> dict:

    prompt = f"""
Create exactly 3 multiple-choice questions
from the educational text below.

Requirements:

1. Exactly 3 questions.
2. Each question must have exactly 4 options.
3. Only one option should be correct.
4. The correct_answer must exactly match one option.
5. Distractors should be plausible.
6. Questions must be based on the supplied text.
7. Add a short explanation for each answer.

Educational text:

{passage}
"""

    raw = generate_json(
        prompt,
        QUIZ_SCHEMA,
        temperature=0.2,
        max_output_tokens=1800,
    )

    raw = clean_json_block(raw)

    data = json.loads(raw)

    quiz = QuizResult.model_validate(data)

    # Additional validation
    for question in quiz.questions:

        if question.correct_answer not in question.options:

            raise ValueError(
                "Generated quiz contains an invalid correct answer."
            )

    return quiz.model_dump()