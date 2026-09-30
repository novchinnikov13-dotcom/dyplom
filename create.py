from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, Tweet


def create_test_users_and_tweets():
    db: Session = SessionLocal()
    try:
        # Проверка, есть ли уже тестовые пользователи
        if db.query(User).filter(User.name == "test_user").first():
            print("Тестовые данные уже существуют.")
            return

        user1 = User(name="test_user")
        user2 = User(name="test_user2")

        db.add_all([user1, user2])
        db.commit()
        db.refresh(user1)
        db.refresh(user2)


        tweets = [
            Tweet(content="Первый тестовый твит", author_id=user1.id),
            Tweet(content="Второй тестовый твит", author_id=user1.id),
            Tweet(content="Твит от второго пользователя", author_id=user2.id),
        ]

        db.add_all(tweets)
        db.commit()

        print("Тестовые данные созданы.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_test_users_and_tweets()