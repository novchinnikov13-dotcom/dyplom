from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    id: int
    name: str


class UserLists(UserBase):
    followers: List[UserBase]
    following: List[UserBase]


class UsersListResponse(BaseModel):
    result: bool
    users: List[UserBase]



class TweetAuth(BaseModel):
    id: int
    name: str


class LikeInfo(BaseModel):
    user_id: int
    name: str


class TweetInfo(BaseModel):
    id: int
    content: str
    attachments: List[str] = []
    author: TweetAuth
    likes: List[LikeInfo] = []


class TweetCreate(BaseModel):
    """Схема создания твита (тело запроса)."""
    tweet_data: str
    tweet_media_ids: Optional[List[int]] = None


class GenericResponse(BaseModel):
    """Базовый ответ с полем result."""
    result: bool


class TweetCreateResponse(GenericResponse):
    """Ответ на создание твита."""
    tweet_id: int


class MediaUploadResponse(GenericResponse):
    """Ответ на загрузку медиа."""
    media_id: int


class TweetsListResponse(GenericResponse):
    """Ответ на получение ленты твитов."""
    tweets: List[TweetInfo]


class UserProfileResponse(GenericResponse):
    """Ответ на получение профиля пользователя."""
    user: UserLists

class ErrorResponse(BaseModel):
    """Схема ошибки."""
    result: bool = False
    error_type: str
    error_message: str
