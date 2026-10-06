
from app.api.tweets import register_endpoints as register_tweets
from app.api.medias import reg_endpoints as register_medias
from app.api.users import reg_endpoints as register_users
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent


def create_app() -> FastAPI:
    _app = FastAPI(
        title="Microblog Backend",
        description="Backend for corporate microblog service (Twitter clone)",
        version="0.1.0",
    )

    BASE_DIR = Path(__file__).resolve().parent.parent
    DEFAULT_API_KEY = "test_user"

    class DefaultApiKeyMiddleware:
        def __init__(self, app, api_key: str):
            self.app = app
            self.api_key = api_key

        async def __call__(self, scope, receive, send):
            if scope["type"] != "http":
                await self.app(scope, receive, send)
                return

            path = scope["path"]

            if path.startswith("/api/"):
                headers = list(scope.get("headers", []))

                has_api_key = any(
                    key.lower() == b"api-key"
                    for key, value in headers
                )

                if not has_api_key:
                    headers.append(
                        (
                            b"api-key",
                            self.api_key.encode("latin-1"),
                        )
                    )

                    scope = dict(scope)
                    scope["headers"] = headers

                    logger.info(
                        "Default api-key added: path=%s",
                        path,
                    )

            await self.app(scope, receive, send)

    _app = FastAPI(
        title="Microblog Backend",
        description="Backend for corporate microblog service",
        version="0.1.0",
    )

    _app.add_middleware(
        DefaultApiKeyMiddleware,
        api_key=DEFAULT_API_KEY,
    )

    _app.mount(
        "/css",
        StaticFiles(directory=BASE_DIR / "static" / "css"),
        name="css",
    )

    _app.mount(
        "/js",
        StaticFiles(directory=BASE_DIR / "static" / "js"),
        name="js",
    )

    @_app.get("/", response_class=HTMLResponse)
    async def index():
        return FileResponse(BASE_DIR / "templates" / "index.html")

    register_tweets(_app)
    register_medias(_app)
    register_users(_app)

    return _app


app = create_app()
