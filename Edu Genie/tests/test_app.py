from fastapi.testclient import TestClient

import main


client = TestClient(main.app)


# ---------------------------------------------------------
# Health test
# ---------------------------------------------------------

def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json()["status"] == "ok"


# ---------------------------------------------------------
# Validation test
# ---------------------------------------------------------

def test_empty_input_rejected():

    response = client.post(

        "/api/task",

        json={
            "task": "qa",
            "text": ""
        }
    )

    assert response.status_code == 422


# ---------------------------------------------------------
# Q&A test
# ---------------------------------------------------------

def test_qa_endpoint(monkeypatch):

    monkeypatch.setattr(
        main,
        "answer_question",
        lambda text: "Mock answer"
    )


    response = client.post(

        "/qa",

        json={
            "task": "qa",
            "text": "What is Python?"
        }
    )


    assert response.status_code == 200


    data = response.json()


    assert data["task"] == "qa"

    assert data["result"] == "Mock answer"


# ---------------------------------------------------------
# Quiz test
# ---------------------------------------------------------

def test_quiz_endpoint(monkeypatch):

    mock_quiz = {

        "questions": [

            {

                "question":
                    "2 + 2 = ?",

                "options": [
                    "3",
                    "4",
                    "5",
                    "6"
                ],

                "correct_answer":
                    "4",

                "explanation":
                    "Two plus two equals four."
            },


            {

                "question":
                    "Capital of France?",

                "options": [
                    "Paris",
                    "Rome",
                    "Berlin",
                    "Madrid"
                ],

                "correct_answer":
                    "Paris",

                "explanation":
                    "Paris is the capital of France."
            },


            {

                "question":
                    "Water formula?",

                "options": [
                    "CO2",
                    "H2O",
                    "O2",
                    "NaCl"
                ],

                "correct_answer":
                    "H2O",

                "explanation":
                    "Water is H2O."
            }
        ]
    }


    monkeypatch.setattr(
        main,
        "generate_quiz",
        lambda text: mock_quiz
    )


    response = client.post(

        "/quiz",

        json={
            "task": "quiz",
            "text": "Basic science"
        }
    )


    assert response.status_code == 200


    data = response.json()


    assert len(
        data["result"]["questions"]
    ) == 3