from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from . import models
from .database import engine, get_db
from .routers import tenants, visitors

"""Instance"""
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

'''Jinja2'''
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
static_dir = str(Path(BASE_DIR, 'static'))
templates_dir = str(Path(BASE_DIR, 'templates'))

templates = Jinja2Templates(directory=templates_dir)
app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")


app.include_router(tenants.router)

@app.get("/")
def home(request: Request):
    # try:
    #     return templates.TemplateResponse("index.html", {"request": request})
    # except Exception as e:
    #     return "Template not found"
    return templates.TemplateResponse("index.html", {"request": request})
