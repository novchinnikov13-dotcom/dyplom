from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from app.config import DATABASE_URL
from app.models import Base
from app.models import User, Tweet



engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

TEST_USERS = [
    {"id": 1, "name": "alice", "followers":[{"id": 2, "name": "bob"}],"following":[{"id": 3, "name": "carol"}, {"id": 2, "name": "bob"}]},
    {"id": 2, "name": "bob"},
    {"id": 3, "name": "carol"},
{"id": 4, "name": "mike"},
]



def get_db() -> Session:
    """создаёт сессию БД для одного запроса"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """    Создаёт все таблицы в БД по моделям (вызывается при старте).
"""
    Base.metadata.create_all(bind=engine)


def create_test_users(db: Session):
    db.execute(text("DELETE FROM users"))
    db.commit()
    for user_data in TEST_USERS:
        existin = db.query(User).filter(User.id == user_data["id"]).first()
        if existin is None:
            user = User(id=user_data["id"], name=user_data["name"])
            db.add(user)
        db.add(user)
    db.commit()
    alice = db.query(User).filter(User.id == 1).first()
    bob = db.query(User).filter(User.id == 2).first()
    carol = db.query(User).filter(User.id == 3).first()
    mike = db.query(User).filter(User.id == 4).first()
    tw_1 = Tweet(author_id=2, content = 'Hello world!')
    tw_2 = Tweet(author_id=3, content = 'Welcome')
    tw_3 = Tweet(author_id=4, content='I thought no more was needed\n'
'Youth to prolong\n'
'Than dumb-bell and foil'
'To keep the body young.'
'Oh, who could have foretold'
'That the heart grows old?'
'Though I have many words,'
'What womans satisfied,'
'I am no longer faint'
'Because at her side?'
'Oh, who could have foretold'
'That the heart grows old?'
'I have not lost desire'
'But the heart that I had,'
'I thought twould burn my body'
'Laid on the death-bed.'
'But who could have foretold'
'That the heart grows old?')
    alice.following.append(bob)
    alice.following.append(carol)
    alice.following.append(mike)
    bob.following.append(alice)
    bob.tweets.append(tw_1)
    carol.tweets.append(tw_2)
    mike.tweets.append(tw_3)
    print(mike)
    print(alice.followers)
    db.commit()
