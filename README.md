# AI Genome Career Map

This repository contains a minimal FastAPI web application that serves as an AI-powered career assessment MVP.

## Features

- Homepage with dark mode design
- Step-by-step survey of 15 questions
- Answers stored in a local SQLite database per user session
- Result page shows a chart and job recommendations

## Running the Application

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the server (the application listens on port `9999` by default):
   ```bash
   uvicorn app.main:app --reload --port 9999
   ```
   Alternatively you can simply run `python app/main.py`.
3. Open `http://localhost:9999` in your browser.

