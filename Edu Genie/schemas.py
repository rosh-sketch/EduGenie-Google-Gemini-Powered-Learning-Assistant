from typing import Any, Literal

from pydantic import BaseModel, Field


TaskName = Literal[
    "qa",
    "explain",
    "quiz",
    "summarize",
    "learn",
]


class TaskRequest(BaseModel):

    task: TaskName

    text: str = Field(
        min_length=1,
        max_length=20000,
    )


class QuizQuestion(BaseModel):

    question: str

    options: list[str] = Field(
        min_length=4,
        max_length=4,
    )

    correct_answer: str

    explanation: str


class QuizResult(BaseModel):

    questions: list[QuizQuestion] = Field(
        min_length=3,
        max_length=3,
    )


class LearningStep(BaseModel):

    level: str

    topic: str

    estimated_time: str

    objectives: list[str]

    resources: list[str]


class LearningPath(BaseModel):

    topic: str

    steps: list[LearningStep]

    study_tips: list[str]


class TaskResponse(BaseModel):

    task: TaskName

    result: Any