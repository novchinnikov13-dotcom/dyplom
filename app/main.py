from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.api.tweets import register_endpoints as register_tweets
from app.api.medias import reg_endpoints as register_medias
from app.api.users import reg_endpoints as register_users
from app.database import SessionLocal, create_test_users


BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="Microblog Backend",
    description="Backend for corporate microblog service (Twitter clone)",
    version="0.1.0",
)

app.mount("/css", StaticFiles(directory=BASE_DIR / "static" / "css"), name="css")
app.mount("/js", StaticFiles(directory=BASE_DIR / "static" / "js"), name="js")

#uvicorn app.main:app --reload


TEMPLATES_DIR = BASE_DIR / "templates"


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    GET /
    Отдаёт главную страницу — HTML файл index.html.
    """
    return FileResponse(TEMPLATES_DIR / "index.html")

db = SessionLocal()
try:
    create_test_users(db)
finally:
    db.close()


register_tweets(app)
register_medias(app)
register_users(app)

