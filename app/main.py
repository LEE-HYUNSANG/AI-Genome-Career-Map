from fastapi import FastAPI, Request, Form, Cookie, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
from uuid import uuid4
from typing import Optional

# Initialize FastAPI app
app = FastAPI()

# Mount static files for CSS and JS
app.mount('/static', StaticFiles(directory='static'), name='static')

# Set up Jinja2 templates
templates = Jinja2Templates(directory='templates')

# Database initialization
DB_PATH = 'career.db'

# List of survey questions (15 total)
QUESTIONS = [
    "I enjoy working with numbers and data analysis.",
    "I prefer hands-on tasks over theoretical ones.",
    "I like helping people solve their problems.",
    "I enjoy creative writing or artistic endeavors.",
    "I am comfortable speaking in front of groups.",
    "I prefer working independently rather than in teams.",
    "I am interested in how machines or software work.",
    "I stay calm under pressure.",
    "I like organizing events or managing projects.",
    "I pay attention to small details in tasks.",
    "I enjoy learning new technologies.",
    "I have an entrepreneurial mindset.",
    "I prefer structured environments and schedules.",
    "I enjoy solving puzzles and complex problems.",
    "I like reading about psychology or human behavior."
]

TOTAL_QUESTIONS = len(QUESTIONS)


def init_db():
    """Create the responses table if it does not exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                q_index INTEGER,
                answer TEXT
            )"""
    )
    conn.commit()
    conn.close()


# Initialize database on startup
init_db()


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    """Render homepage."""
    return templates.TemplateResponse('index.html', {'request': request})


@app.get('/survey', response_class=HTMLResponse)
async def get_survey(request: Request, q: int = 0, session_id: Optional[str] = Cookie(None)):
    """Display survey question by index."""
    if session_id is None:
        session_id = str(uuid4())
    if q >= TOTAL_QUESTIONS:
        return RedirectResponse(url='/result', status_code=302)
    question = QUESTIONS[q]
    progress = int((q / TOTAL_QUESTIONS) * 100)
    response = templates.TemplateResponse(
        'survey.html',
        {
            'request': request,
            'question': question,
            'q_index': q,
            'total': TOTAL_QUESTIONS,
            'progress': progress
        }
    )
    response.set_cookie('session_id', session_id)
    return response


@app.post('/survey')
async def post_survey(
    request: Request,
    q_index: int = Form(...),
    answer: str = Form(...),
    session_id: Optional[str] = Cookie(None)
):
    """Store answer and redirect to next question."""
    if session_id is None:
        session_id = str(uuid4())
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        'INSERT INTO responses (session_id, q_index, answer) VALUES (?, ?, ?)',
        (session_id, q_index, answer)
    )
    conn.commit()
    conn.close()
    next_q = int(q_index) + 1
    if next_q >= TOTAL_QUESTIONS:
        return RedirectResponse(url='/result', status_code=302)
    return RedirectResponse(url=f'/survey?q={next_q}', status_code=302)


@app.get('/result', response_class=HTMLResponse)
async def result(request: Request, session_id: Optional[str] = Cookie(None)):
    """Generate and display result report."""
    if session_id is None:
        return RedirectResponse(url='/', status_code=302)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        'SELECT q_index, answer FROM responses WHERE session_id = ? ORDER BY q_index',
        (session_id,)
    )
    rows = c.fetchall()
    conn.close()
    if len(rows) < TOTAL_QUESTIONS:
        return RedirectResponse(url='/survey', status_code=302)

    # Simple scoring: count positive answers for different categories
    numeric_answers = [int(r[1]) for r in rows]
    tech = sum(numeric_answers[i] for i in [0, 6, 10, 13])
    people = sum(numeric_answers[i] for i in [2, 4, 7, 14])
    creative = sum(numeric_answers[i] for i in [3, 9, 11])
    management = sum(numeric_answers[i] for i in [8, 12])

    recommendations = []
    if tech >= max(people, creative, management):
        recommendations.append('Consider careers in data science, software engineering, or AI research.')
    if people >= max(tech, creative, management):
        recommendations.append('Roles like counseling, HR, or education might suit you.')
    if creative >= max(tech, people, management):
        recommendations.append('Look into writing, design, or marketing careers.')
    if management >= max(tech, people, creative):
        recommendations.append('Project management or operations could be a good fit.')
    if not recommendations:
        recommendations.append('Explore interdisciplinary roles that combine multiple interests.')

    chart_data = {
        'labels': ['Tech', 'People', 'Creative', 'Management'],
        'scores': [tech, people, creative, management]
    }

    return templates.TemplateResponse(
        'result.html',
        {
            'request': request,
            'chart_data': chart_data,
            'recommendations': recommendations,
            'session_id': session_id
        }
    )

