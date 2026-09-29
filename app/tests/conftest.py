import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import User, Tweet, Likes

# Тестовая БД — SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Переопределяем зависимость get_db в приложении
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def create_tables_and_seed():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        alice = User(name="alice")
        bob = User(name="bob")
        carol = User(name="carol")
        db.add_all([alice, bob, carol])
        db.flush()

        alice.following.append(bob)
        alice.following.append(carol)

        t1 = Tweet(author_id=alice.id, content="Hello from Alice!")
        t2 = Tweet(author_id=bob.id, content="Bob here.")
        t3 = Tweet(author_id=carol.id, content="Carol tweeting.")
        db.add_all([t1, t2, t3])
        db.flush()

        like = Likes(user_id=bob.id, tweet_id=t1.id)
        db.add(like)

        db.commit()

        all_users = db.query(User).all()
        print("Users in test DB:", [u.name for u in all_users])
    finally:
        db.close()

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as c:
        yield c