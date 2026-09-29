from fastapi import FastAPI, Header, HTTPException, Request, Depends, Cookie, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import (
    UserLists,
    UserProfileResponse,
    GenericResponse,
    UserBase, UsersListResponse,
)


# def get_user_by_api_key(db: Session, api_key: str) -> User:
#     user = db.query(User).filter(User.name == api_key).first()
#     if user is None:
#         raise HTTPException(
#                 status_code=401,
#                 detail={
#                     "result": False,
#                     "error_type": "unauthorized",
#                     "error_message": "Invalid api-key",
#                 },
#             )
#     return user

def get_default_user(db: Session = Depends(get_db)) -> User:

    user = db.query(User).first()
    if user is None:
        raise HTTPException(500, detail="No users in DB")
    return user

# def get_current_user_from_cookie(
#     api_key: str | None = Cookie(None, alias="api_key"),
#     db: Session = Depends(get_db),) -> User:
#     if not api_key:
#         raise HTTPException(
#             status_code=401,
#             detail={
#                 "result": False,
#                 "error_type": "unauthorized",
#                 "error_message": "No api_key cookie",
#                 },
#             )
#     return get_user_by_api_key(db, api_key)




def reg_endpoints(app: FastAPI) -> None:
    @app.get("/api/users", response_model=UsersListResponse)
    def get_all_users(db: Session = Depends(get_db)):
        users = db.query(User).all()
        users_list = [UserBase(id=u.id, name=u.name) for u in users]
        return UsersListResponse(result=True, users=users_list)


    @app.get("/api/users/me", response_model=UserProfileResponse)
    def get_me_profile(current_user: User = Depends(get_default_user),
                       db: Session = Depends(get_db),) -> UserProfileResponse:
        user_details = UserLists(
            id=current_user.id,
            name=current_user.name,
            followers=[
                UserBase(id=u.id, name=u.name)
                for u in current_user.followers
            ],
            following=[
                UserBase(id=u.id, name=u.name)
                for u in current_user.following
            ],
        )
        return UserProfileResponse(result=True, user=user_details)


    @app.post("/api/users/{user_id}/follow", response_model=GenericResponse)
    def follow_user(user_id: int, current_user: User = Depends(get_default_user),
                       db: Session = Depends(get_db), ) -> GenericResponse:
        """
        Подписаться на пользователя.
        :param user_id:
        :param api_key:
        :return:
        """
        if user_id == current_user.id:
            raise HTTPException(
                status_code=400,
                detail={
                    "result": False,
                    "error_type": "bad_request",
                    "error_message": "Cannot follow yourself",
                },
            )
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if user is None:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "result": False,
                        "error_type": "not_found",
                        "error_message": "User not found",
                    },
                )
            if user not in current_user.following:
                current_user.following.append(user)
                db.commit()

            return GenericResponse(result=True)
        except Exception:
            db.rollback()
            raise

        finally:
            db.close()


    @app.delete("/api/users/{user_id}/follow", response_model=GenericResponse)
    def unfollow_user(
        user_id: int, current_user: User = Depends(get_default_user),
                       db: Session = Depends(get_db), ) -> GenericResponse:
        """
         Отписаться от пользователя.
        :param user_id:
        :param api_key:
        :return:
        """


        try:
            user_for_del = db.query(User).filter(User.id == user_id).first()
            if user_for_del is None:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "result": False,
                        "error_type": "not_found",
                        "error_message": "User not found",
                    },
                )

            if user_for_del in current_user.following:
                current_user.following.remove(user_for_del)
                db.commit()
            return GenericResponse(result=True)
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    @app.get("/api/users/{user_id}", response_model=UserProfileResponse)
    def get_user_profile(
            user_id: int,
            db: Session = Depends(get_db),
    ) -> UserProfileResponse:
        user = db.query(User).filter(User.id == user_id).first()
        user_det = UserLists(id= user.id, name=user.name, followers=[UserBase(id=u.id, name=u.name)
            for u in user.followers], following=[UserBase(id=u.id, name=u.name)
            for u in user.following],)
        return UserProfileResponse(result=True, user=user_det)