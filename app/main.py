from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse('00_home.html', {'request': request})

@app.get('/service', response_class=HTMLResponse)
async def service(request: Request):
    return templates.TemplateResponse('01_service.html', {'request': request})

@app.get('/diagnostics', response_class=HTMLResponse)
async def diagnostics(request: Request):
    return templates.TemplateResponse('02_diagnostics.html', {'request': request})

@app.get('/result', response_class=HTMLResponse)
async def result(request: Request):
    return templates.TemplateResponse('03_result.html', {'request': request})

@app.get('/resources', response_class=HTMLResponse)
async def resources(request: Request):
    return templates.TemplateResponse('04_resources.html', {'request': request})

@app.get('/community', response_class=HTMLResponse)
async def community(request: Request):
    return templates.TemplateResponse('05_community.html', {'request': request})

@app.get('/partners', response_class=HTMLResponse)
async def partners(request: Request):
    return templates.TemplateResponse('06_partners.html', {'request': request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9999)
