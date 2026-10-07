import uuid
from pathlib import Path

from fastapi import (
    Depends,
    FastAPI,
    File,
    Header,
    UploadFile,
)
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.config import MEDIA_ROOT
from app.database import get_db
from app.models import Media, User
from app.schemas import GenericResponse, MediaUploadResponse


def get_user_by_api_key(
    db: Session,
    api_key: str | None,
) -> User | None:
    if not api_key:
        return None

    return db.query(User).filter(User.name == api_key).first()


def reg_endpoints(app: FastAPI) -> None:
    media_root = Path(MEDIA_ROOT)
    media_root.mkdir(parents=True, exist_ok=True)

    app.mount(
        "/media",
        StaticFiles(directory=media_root),
        name="media",
    )

    @app.post(
        "/api/medias",
        response_model=MediaUploadResponse,
    )
    def upload_media(
        file: UploadFile = File(...),
        api_key: str | None = Header(
            default=None,
            alias="api-key",
        ),
        db: Session = Depends(get_db),
    ) -> MediaUploadResponse:
        current_user = get_user_by_api_key(db, api_key)

        if current_user is None:
            return MediaUploadResponse(
                result=False,
                error_type="unauthorized",
                error_message="Invalid api-key",
            )

        if not file.filename:
            return MediaUploadResponse(
                result=False,
                error_type="bad_request",
                error_message="Filename is required",
            )

        if not file.content_type or not file.content_type.startswith("image/"):
            return MediaUploadResponse(
                result=False,
                error_type="bad_request",
                error_message="Only image files are allowed",
            )

        extension = Path(file.filename).suffix.lower()

        if not extension:
            extension = ".jpg"

        filename = f"{uuid.uuid4().hex}{extension}"
        file_path = media_root / filename

        try:
            with file_path.open("wb") as output_file:
                while chunk := file.file.read(1024 * 1024):
                    output_file.write(chunk)

            media = Media(
                owner_id=current_user.id,
                filename=file.filename,
                path=f"/media/{filename}",
            )

            db.add(media)
            db.commit()
            db.refresh(media)

            return MediaUploadResponse(
                result=True,
                media_id=media.id,
            )

        except Exception:
            db.rollback()

            if file_path.exists():
                file_path.unlink()

            raise

        finally:
            file.file.close()

    @app.post(
        "/api/medias/upload",
        response_model=MediaUploadResponse,
        include_in_schema=False,
    )
    def upload_media_legacy(
        file: UploadFile = File(...),
        api_key: str | None = Header(
            default=None,
            alias="api-key",
        ),
        db: Session = Depends(get_db),
    ) -> MediaUploadResponse:
        return upload_media(
            file=file,
            api_key=api_key,
            db=db,
        )

    @app.delete(
        "/api/medias/{media_id}",
        response_model=GenericResponse,
    )
    def delete_media(
        media_id: int,
        api_key: str | None = Header(
            default=None,
            alias="api-key",
        ),
        db: Session = Depends(get_db),
    ) -> GenericResponse:
        current_user = get_user_by_api_key(db, api_key)

        if current_user is None:
            return GenericResponse(
                result=False,
                error_type="unauthorized",
                error_message="Invalid api-key",
            )

        media = db.query(Media).filter(Media.id == media_id).first()

        if media is None:
            return GenericResponse(
                result=False,
                error_type="not_found",
                error_message="Media not found",
            )

        if media.owner_id != current_user.id:
            return GenericResponse(
                result=False,
                error_type="forbidden",
                error_message="You can delete only your own media",
            )

        filename = Path(media.path).name
        file_path = media_root / filename

        if file_path.exists():
            file_path.unlink()

        db.delete(media)
        db.commit()

        return GenericResponse(result=True)
