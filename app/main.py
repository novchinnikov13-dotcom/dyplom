from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.api.tweets import register_endpoints as register_tweets
from app.api.medias import reg_endpoints as register_medias
from app.api.users import reg_endpoints as register_users


BASE_DIR = Path(__file__).resolve().parent.parent


def create_app() -> FastAPI:
    """Factory function to create FastAPI application."""
    _app = FastAPI(
        title="Microblog Backend",
        description="Backend for corporate microblog service (Twitter clone)",
        version="0.1.0",
    )

    _app.mount("/css", StaticFiles(directory=BASE_DIR / "static" / "css"), name="css")
    _app.mount("/js", StaticFiles(directory=BASE_DIR / "static" / "js"), name="js")

    @_app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        return FileResponse(BASE_DIR / "templates" / "index.html")

    register_tweets(_app)
    register_medias(_app)
    register_users(_app)

    return _app


app = create_app()
