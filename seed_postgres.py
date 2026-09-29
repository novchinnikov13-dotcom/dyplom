from app.database import Base, SessionLocal, engine
from app.models import User, Tweet

Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    alice = db.query(User).filter_by(name="alice").first()
    if alice is None:
        alice = User(name="alice")
        db.add(alice)

    bob = db.query(User).filter_by(name="bob").first()
    if bob is None:
        bob = User(name="bob")
        db.add(bob)

    carol = db.query(User).filter_by(name="carol").first()
    if carol is None:
        carol = User(name="carol")
        db.add(carol)

    db.flush()

    if bob not in alice.following:
        alice.following.append(bob)
    if carol not in alice.following:
        alice.following.append(carol)

    if not db.query(Tweet).filter_by(content="Bob here.").first():
        db.add(Tweet(author_id=bob.id, content="Bob here."))

    if not db.query(Tweet).filter_by(content="Carol tweeting.").first():
        db.add(Tweet(author_id=carol.id, content="Carol tweeting."))

    db.commit()
    print("PostgreSQL initialized: alice, bob, carol created.")
finally:
    db.close()