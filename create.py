from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine
from app.models import User, Tweet


def create_test_users_and_tweets():
    print("Создание таблиц...")
    Base.metadata.create_all(bind=engine)
    print("Таблицы созданы")

    db: Session = SessionLocal()
    try:
        if db.query(User).first():
            print("БД уже инициализирована.")
            return

        user_test = User(name="test")
        user_alice = User(name="alice")
        user_bob = User(name="bob")
        user_carol = User(name="carol")

        db.add_all([user_test, user_alice, user_bob, user_carol])
        db.flush()

        user_test.following.extend([user_alice, user_bob, user_carol])
        db.commit()

        tweets = [
            Tweet(author_id=user_alice.id, content="Первый твит от alice"),
            Tweet(author_id=user_alice.id, content="Второй твит от alice"),
            Tweet(author_id=user_bob.id, content="Твит от bob"),
            Tweet(author_id=user_carol.id, content="Твит от carol"),
        ]
        db.add_all(tweets)
        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Ошибка инициализации: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_test_users_and_tweets()