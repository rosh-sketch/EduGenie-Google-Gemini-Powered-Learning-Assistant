from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from schemas import TaskRequest, TaskResponse
from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)


# ---------------------------------------------------------
# Static files
# ---------------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)


# ---------------------------------------------------------
# Templates
# ---------------------------------------------------------

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# ---------------------------------------------------------
# Home page
# ---------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "EduGenie"
        },
    )


# ---------------------------------------------------------
# Health check
# ---------------------------------------------------------

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "EduGenie"
    }


# ---------------------------------------------------------
# Main task endpoint
# ---------------------------------------------------------

@app.post("/api/task", response_model=TaskResponse)
async def run_task(payload: TaskRequest):

    task = payload.task
    text = payload.text.strip()

    if task == "qa":
        result = answer_question(text)

    elif task == "explain":
        result = explain_topic(text)

    elif task == "quiz":
        result = generate_quiz(text)

    elif task == "summarize":
        result = summarize_text(text)

    elif task == "learn":
        result = get_learning_recommendations(text)

    else:
        raise ValueError(
            f"Unsupported task: {task}"
        )

    return TaskResponse(
        task=task,
        result=result
    )


# ---------------------------------------------------------
# Individual REST endpoints
# These match the endpoints described in the documentation.
# ---------------------------------------------------------

@app.post("/qa", response_model=TaskResponse)
async def qa(payload: TaskRequest):

    payload.task = "qa"

    return await run_task(payload)


@app.post("/explain", response_model=TaskResponse)
async def explain(payload: TaskRequest):

    payload.task = "explain"

    return await run_task(payload)


@app.post("/quiz", response_model=TaskResponse)
async def quiz(payload: TaskRequest):

    payload.task = "quiz"

    return await run_task(payload)


@app.post("/summarize", response_model=TaskResponse)
async def summarize(payload: TaskRequest):

    payload.task = "summarize"

    return await run_task(payload)


@app.post("/learn/recommendations", response_model=TaskResponse)
async def recommendations(payload: TaskRequest):

    payload.task = "learn"

    return await run_task(payload)