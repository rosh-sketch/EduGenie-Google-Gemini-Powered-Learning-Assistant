import json

from ai_client import generate_json

from schemas import LearningPath


LEARNING_SCHEMA = {

    "type": "object",

    "properties": {

        "topic": {
            "type": "string"
        },

        "steps": {

            "type": "array",

            "minItems": 4,

            "maxItems": 8,

            "items": {

                "type": "object",

                "properties": {

                    "level": {
                        "type": "string"
                    },

                    "topic": {
                        "type": "string"
                    },

                    "estimated_time": {
                        "type": "string"
                    },

                    "objectives": {

                        "type": "array",

                        "items": {
                            "type": "string"
                        },
                    },

                    "resources": {

                        "type": "array",

                        "items": {
                            "type": "string"
                        },
                    },
                },

                "required": [
                    "level",
                    "topic",
                    "estimated_time",
                    "objectives",
                    "resources",
                ],
            },
        },

        "study_tips": {

            "type": "array",

            "minItems": 3,

            "maxItems": 6,

            "items": {
                "type": "string"
            },
        },
    },

    "required": [
        "topic",
        "steps",
        "study_tips",
    ],
}


def get_learning_recommendations(topic: str) -> dict:

    prompt = f"""
Create a personalized learning path
for the following topic:

{topic}

The learning path must:

1. Start from beginner level.
2. Progress toward intermediate level.
3. Progress toward advanced level.
4. Include multiple learning steps.
5. Give an estimated time for each step.
6. Give learning objectives.
7. Suggest useful resource types or known resources.
8. Do not fabricate URLs.
9. Give practical study tips.
10. Make the sequence suitable for a self-learner.
"""

    raw = generate_json(
        prompt,
        LEARNING_SCHEMA,
        temperature=0.35,
        max_output_tokens=2200,
    )

    data = json.loads(raw)

    learning_path = LearningPath.model_validate(
        data
    )

    return learning_path.model_dump()