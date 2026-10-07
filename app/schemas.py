from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    name: str


class UserLists(UserBase):
    followers: list[UserBase]
    following: list[UserBase]


class UsersListResponse(BaseModel):
    result: bool
    users: list[UserBase]


class TweetAuth(BaseModel):
    id: int
    name: str


class LikeInfo(BaseModel):
    user_id: int
    name: str


class TweetInfo(BaseModel):
    id: int
    content: str
    attachments: list[str] = []
    author: TweetAuth
    likes: list[LikeInfo] = []


class TweetCreate(BaseModel):
    """Схема создания твита (тело запроса)."""

    tweet_data: str
    tweet_media_ids: list[int] | None = None


class GenericResponse(BaseModel):
    """Базовый ответ с полем result."""
    result: bool
    error_type: str | None = None
    error_message: str | None = None


class TweetCreateResponse(BaseModel):
    """Ответ на создание твита."""
    result: bool
    error_type: str | None = None
    error_message: str | None = None
    tweet_id: int | None = None


class MediaUploadResponse(GenericResponse):
    """Ответ на загрузку медиа."""

    media_id: int
    error_type: str | None = None
    error_message: str | None = None


class TweetsListResponse(GenericResponse):
    """Ответ на получение ленты твитов."""

    tweets: list[TweetInfo]


class UserProfileResponse(BaseModel):
    """Ответ на получение профиля пользователя."""

    result: bool
    error_type: str | None = None
    error_message: str | None = None
    user: UserLists | None = None
