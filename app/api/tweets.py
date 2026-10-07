from fastapi import Depends, FastAPI, Header
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Likes, Media, Tweet, User
from app.schemas import (
    GenericResponse,
    LikeInfo,
    TweetAuth,
    TweetCreate,
    TweetCreateResponse,
    TweetInfo,
    TweetsListResponse,
)


def get_user_by_api(db: Session, api_key: str) -> User:
    user = db.query(User).filter(User.name == api_key).first()
    if user is None:
        return None

    return user


# def get_default_user(db: Session = Depends(get_db)) -> User:
#
#     user = db.query(User).first()
#     if user is None:
#         raise HTTPException(500, detail="No users in DB")
#     return user


def register_endpoints(app: FastAPI) -> None:
    @app.post("/api/tweets", response_model=TweetCreateResponse)
    def create_tweet(
        body: TweetCreate,
        api_key: str = Header(..., alias="api-key"),
        db: Session = Depends(get_db),
    ) -> TweetCreateResponse:
        current_user = get_user_by_api(db, api_key)
        if current_user is None:
            return TweetCreateResponse(
                result=False,
                error_type="unauthorized",
                error_message="Invalid api-key",
                tweet_id=None,
            )
        tweet = Tweet(author_id=current_user.id, content=body.tweet_data)
        db.add(tweet)
        db.flush()

        if body.tweet_media_ids:
            media_list = (
                db.query(Media)
                .filter(
                    Media.id.in_(body.tweet_media_ids),
                    Media.owner_id == current_user.id,
                )
                .all()
            )
            tweet.media.extend(media_list)
        db.commit()

        return TweetCreateResponse(result=True, tweet_id=tweet.id)

    @app.get("/api/tweets", response_model=TweetsListResponse)
    def get_data(
        api_key: str = Header(..., alias="api-key"),
        db: Session = Depends(get_db),
    ) -> TweetsListResponse:
        current_user = get_user_by_api(db, api_key)
        if current_user is None:
            return TweetsListResponse(
                result=False,
                error_type="unauthorized",
                error_message="Invalid api-key",
                tweets=[],
            )
        following_id = [u.id for u in current_user.following]
        following_id.append(current_user.id)
        tweets = (
            db.query(Tweet)
            .filter(Tweet.author_id.in_(following_id))
            .outerjoin(Likes, Tweet.id == Likes.tweet_id)
            .group_by(Tweet.id)
            .order_by(func.count(Likes.id).desc())
            .all()
        )

        def tweet_to_info(t: Tweet) -> TweetInfo:
            return TweetInfo(
                id=t.id,
                content=t.content,
                author=TweetAuth(id=t.author.id, name=t.author.name),
                likes=[
                    LikeInfo(user_id=like.user.id, name=like.user.name)
                    for like in t.likes
                ],
                attachments=[media.path for media in t.media if media.path],
            )

        tweets_l = [tweet_to_info(t) for t in tweets]
        return TweetsListResponse(result=True, tweets=tweets_l)

    @app.delete("/api/tweets/{tweet_id}", response_model=GenericResponse)
    def delete_tweet(
        tweet_id: int,
        api_key: str = Header(..., alias="api-key"),
        db: Session = Depends(get_db),
    ) -> GenericResponse:
        current_user = get_user_by_api(db, api_key)
        if current_user is None:
            return GenericResponse(
                result=False,
                error_type="unauthorized",
                error_message="Invalid api-key",
            )
        tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()
        if tweet is None:
            return GenericResponse(
                result=False,
                error_type="not_found",
                error_message="Tweet not found",
            )
        if tweet.author_id != current_user.id:
            return GenericResponse(
                result=False,
                error_type="not_found",
                error_message="Tweet not found",
            )

        db.delete(tweet)
        db.commit()

        return GenericResponse(result=True)

    @app.post("/api/tweets/{tweet_id}/likes", response_model=GenericResponse)
    def tweet_like(
        tweet_id: int,
        api_key: str = Header(..., alias="api-key"),
        db: Session = Depends(get_db),
    ) -> GenericResponse:
        current_user = get_user_by_api(db, api_key)
        if current_user is None:
            return GenericResponse(
                result=False,
                error_type="unauthorized",
                error_message="Invalid api-key",
            )
        tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()
        if tweet is None:
            return GenericResponse(
                result=False,
                error_type="not_found",
                error_message="Tweet not found",
            )

        exist = (
            db.query(Likes)
            .filter(Likes.tweet_id == tweet_id, Likes.user_id == current_user.id)
            .first()
        )
        if exist:
            return GenericResponse(result=True)

        like = Likes(user_id=current_user.id, tweet_id=tweet_id)
        db.add(like)
        db.commit()

        return GenericResponse(result=True)

    @app.delete("/api/tweets/{tweet_id}/likes", response_model=GenericResponse)
    def del_like(
        tweet_id: int,
        api_key: str = Header(..., alias="api-key"),
        db: Session = Depends(get_db),
    ) -> GenericResponse:
        current_user = get_user_by_api(db, api_key)
        if current_user is None:
            return GenericResponse(
                result=False,
                error_type="unauthorized",
                error_message="Invalid api-key",
            )
        tweet = db.query(Tweet).filter(Tweet.id == tweet_id).first()
        if tweet is None:
            return GenericResponse(
                result=False,
                error_type="not_found",
                error_message="Tweet not found",
            )

        like = (
            db.query(Likes)
            .filter(Likes.tweet_id == tweet_id, Likes.user_id == current_user.id)
            .first()
        )
        if like:
            db.delete(like)
            db.commit()

        return GenericResponse(result=True)
