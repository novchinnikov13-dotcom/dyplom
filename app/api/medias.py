import os
import uuid

from fastapi import FastAPI, Header, UploadFile, File, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.database import SessionLocal
from app.models import User, Media
from app.schemas import MediaUploadResponse
from app.config import MEDIA_ROOT

# def get_user_by_api_key(db: Session, api_key: str) -> User:
#     """
#     Вспомогательная функция: ищет пользователя по заголовку api-key.
#     """
#     user = db.query(User).filter(User.name == api_key).first()
#     if user is None:
#         raise HTTPException(
#             status_code=401,
#             detail={
#                 "result": False,
#                 "error_type": "unauthorized",
#                 "error_message": "Invalid api-key",
#             },
#         )
#     return user


def get_default_user(db: Session = Depends(get_db)) -> User:
    user = db.query(User).first()
    if user is None:
        raise HTTPException(500, detail="No users in DB")
    return user

def reg_endpoints(app: FastAPI) -> None:
    @app.post("/api/medias", response_model=MediaUploadResponse)
    def upload_media(current_user: User = Depends(get_default_user), file: UploadFile = File(...), db: Session = Depends(get_db)
    ) -> MediaUploadResponse:
        """
        POST /api/medias
        Загрузка медиафайла (картинки) для твита.
        :return:
        """

        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail={
                    "result": False,
                    "error_type": "bad_request",
                    "error_message": "Only image files are allowed",
                },
            )
        os.makedirs(MEDIA_ROOT, exist_ok=True)
        format = os.path.splitext(file.filename)[1].lower() if file.filename else '.jpg'
        filename = f"{uuid.uuid4().hex}{format}"
        path = os.path.join(MEDIA_ROOT, filename)

        with open(path, 'wb') as media:
            media.write(file.file.read())


        try:
            media = Media(owner_id = current_user.id, filename = file.filename,
                          path = f"/media/{filename}",)
            db.add(media)
            db.commit()
            db.refresh(media)
            return MediaUploadResponse(result=True, media_id=media.id)
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

