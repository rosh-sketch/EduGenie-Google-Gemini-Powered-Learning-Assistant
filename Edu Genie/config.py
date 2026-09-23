import os

from dotenv import load_dotenv


load_dotenv()


APP_NAME = "EduGenie"


GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
).strip()


GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
)


USE_LOCAL_EXPLAINER = (
    os.getenv(
        "USE_LOCAL_EXPLAINER",
        "false"
    ).lower()
    == "true"
)


LOCAL_EXPLAINER_MODEL = os.getenv(
    "LOCAL_EXPLAINER_MODEL",
    "MBZUAI/LaMini-Flan-T5-783M"
)


MAX_INPUT_CHARS = int(
    os.getenv(
        "MAX_INPUT_CHARS",
        "20000"
    )
)