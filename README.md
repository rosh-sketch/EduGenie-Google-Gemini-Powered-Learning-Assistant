# EduGenie – Google Gemini Powered Learning Assistant

**Project Type:** Generative AI / Web Application  
**Team Leader:** Roshan P  
**Team ID:** SWTID-2026-4072  
**Academic Year:** 2026

## Project Overview
EduGenie is a Generative AI-based educational web application designed to help students learn using artificial intelligence. It combines a simple web interface with a FastAPI backend and Google Gemini.

### Main Features
- Question and Answer
- Simplified concept explanation
- Quiz generation
- Text summarization
- Personalized learning recommendations

## System Design
The browser sends a selected task and input to FastAPI. FastAPI routes the request to the appropriate feature module and uses the shared Gemini client where applicable. The generated result is displayed in the browser.

## Technologies Used
| Technology | Purpose |
|---|---|
| Python | Main programming language |
| FastAPI | Backend API framework |
| Uvicorn | Local application server |
| Google Gemini | Generative AI |
| HTML/CSS/JavaScript | Frontend |
| Jinja2 | HTML templating |
| Pydantic | Data validation |
| Pytest | Testing |

## Run the Project
```bash
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000` in a browser.

## Project Structure
```text
EduGenie/
├── main.py
├── config.py
├── ai_client.py
├── schemas.py
├── qna.py
├── explanation_module.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
└── tests/
    ├── __init__.py
    └── test_app.py
```

## Documentation Images

### FastAPI Server
![FastAPI server](images/figure_page_9.jpg)

### EduGenie Interface
![EduGenie interface](images/figure_page_12.jpg)

### Explanation Demonstration
![Explanation demonstration](images/figure_page_15.jpg)

### Quiz Demonstration
![Quiz demonstration](images/figure_page_16.jpg)

## Full Project Documentation
The complete documentation is available as [`EduGenie_Project_Documentation.pdf`](EduGenie_Project_Documentation.pdf).

> **Security:** Do not upload `.env` or your Gemini API key to GitHub. Keep `.env` ignored by `.gitignore` and commit only `.env.example`.
