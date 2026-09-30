import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.database import Base, get_db
import app.models
from app.models import User, Tweet
from app.main import create_app

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    alice = User(name="alice")
    bob = User(name="bob")
    carol = User(name="carol")

    # Алиса подписывается на Боба и Кэрол
    alice.following.append(bob)
    alice.following.append(carol)

    tweets = [
        Tweet(content="Alice hi", author=alice),
        Tweet(content="Here Bob", author=bob),
        Tweet(content="Hello world", author=carol),
    ]

    session.add_all([alice, bob, carol])
    session.add_all(tweets)
    session.commit()

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    _app = create_app()
    _app.dependency_overrides[get_db] = override_get_db

    with TestClient(_app) as test_client:
        yield test_client

    _app.dependency_overrides.clear()

