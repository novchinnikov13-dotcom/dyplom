from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Table, Boolean,
)
from sqlalchemy.orm import relationship
from app.database import Base

follows = Table('follows', Base.metadata,
Column('follower_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('following_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
                )

tweet_media = Table('tweet_media', Base.metadata,
                    Column('tweet_id', Integer, ForeignKey('tweets.id', ondelete='CASCADE'), primary_key=True),
                    Column('media_id', Integer, ForeignKey('media.id', ondelete='CASCADE'), primary_key=True),

                    )

class User(Base):
    """
      Модель пользователя.
      """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)

    tweets = relationship('Tweet', back_populates='author', cascade='all, delete-orphan')
    media = relationship('Media', back_populates='owner', cascade='all, delete-orphan')
    likes = relationship('Likes', back_populates='user', cascade='all, delete-orphan')
    following = relationship(
        "User",
        secondary=follows,
        primaryjoin=id == follows.c.follower_id,
        secondaryjoin=id == follows.c.following_id,
        backref="followers",
    )


class Tweet(Base):
    """Модель твита."""

    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    author = relationship('User', back_populates='tweets')
    media = relationship('Media', secondary=tweet_media, backref='tweets')
    likes = relationship('Likes', back_populates='tweet', cascade='all, delete-orphan')


class Media(Base):
    """
 Модель медиафайла (картинки).
    """
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    filename = Column(String, nullable=False)
    path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    owner = relationship('User', back_populates='media')


class Likes(Base):
    """
       Модель лайка.
       """
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    tweet_id = Column(Integer, ForeignKey('tweets.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship('User', back_populates='likes')
    tweet = relationship('Tweet', back_populates='likes')
