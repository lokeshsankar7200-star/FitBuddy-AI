from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path

from .routes import router


app = FastAPI(
    title="FitBuddy-AI Fitness Plan Generator",
    description="AI-powered fitness plan generator"
)

BASE_DIR = Path(__file__).resolve().parent.parent


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


@app.get("/", response_class=HTMLResponse)
async def home():

    html_file = BASE_DIR / "templates" / "index.html"

    return html_file.read_text(encoding="utf-8")


app.include_router(router)