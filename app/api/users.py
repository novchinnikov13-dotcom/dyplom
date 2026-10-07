from fastapi import Depends, FastAPI, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import (
    GenericResponse,
    UserBase,
    UserLists,
    UserProfileResponse,
    UsersListResponse,
)


def get_user_by_api_key(
    db: Session,
    api_key: str | None,
) -> User | None:
    if not api_key:
        return None

    return db.query(User).filter(User.name == api_key).first()


def get_current_user(
    api_key: str | None = Header(
        default=None,
        alias="api-key",
    ),
    db: Session = Depends(get_db),
) -> User:
    user = get_user_by_api_key(db, api_key)

    return user


def reg_endpoints(app: FastAPI) -> None:

    @app.get(
        "/api/users",
        response_model=UsersListResponse,
    )
    @app.get(
        "/api/users/",
        response_model=UsersListResponse,
        include_in_schema=False,
    )
    def get_all_users(
        api_key: str | None = Header(
            default=None,
            alias="api-key",
        ),
        db: Session = Depends(get_db),
    ):
        users = db.query(User).all()

        users_list = [UserBase(id=user.id, name=user.name) for user in users]

        return UsersListResponse(
            result=True,
            users=users_list,
        )

    @app.get(
        "/api/users/me",
        response_model=UserProfileResponse,
    )
    def get_me_profile(
        current_user: User = Depends(get_current_user),
    ) -> UserProfileResponse:
        if current_user is None:
            return UserProfileResponse(
                result=False,
                error_type="unauthorized",
                error_message="Invalid api-key",
                user=None,
            )
        user_details = UserLists(
            id=current_user.id,
            name=current_user.name,
            followers=[
                UserBase(id=user.id, name=user.name) for user in current_user.followers
            ],
            following=[
                UserBase(id=user.id, name=user.name) for user in current_user.following
            ],
        )

        return UserProfileResponse(
            result=True,
            user=user_details,
        )

    @app.get(
        "/api/users/{user_id}",
        response_model=UserProfileResponse,
    )
    def get_user_profile(
        user_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> UserProfileResponse:
        if current_user is None:
            return UserProfileResponse(
                result=False,
                error_type="unauthorized",
                error_message="Invalid api-key",
                user=None,
            )
        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            return UserProfileResponse(
                result=False,
                error_type="not_found",
                error_message="User not found",
            )

        user_details = UserLists(
            id=user.id,
            name=user.name,
            followers=[UserBase(id=item.id, name=item.name) for item in user.followers],
            following=[UserBase(id=item.id, name=item.name) for item in user.following],
        )

        return UserProfileResponse(
            result=True,
            user=user_details,
        )

    @app.post(
        "/api/users/{user_id}/follow",
        response_model=GenericResponse,
    )
    def follow_user(
        user_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> GenericResponse:
        if user_id == current_user.id:
            return GenericResponse(
                result=False,
                error_type="bad_request",
                error_message="Cannot follow yourself",
            )

        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            return GenericResponse(
                result=False,
                error_type="not_found",
                error_message="User not found",
            )

        if user not in current_user.following:
            current_user.following.append(user)
            db.commit()

        return GenericResponse(result=True)

    @app.delete(
        "/api/users/{user_id}/follow",
        response_model=GenericResponse,
    )
    def unfollow_user(
        user_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> GenericResponse:
        if current_user is None:
            return GenericResponse(
                result=False,
                error_type="unauthorized",
                error_message="Invalid api-key",
            )
        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            return GenericResponse(
                result=False,
                error_type="not_found",
                error_message="User not found",
            )

        if user in current_user.following:
            current_user.following.remove(user)
            db.commit()

        return GenericResponse(result=True)
