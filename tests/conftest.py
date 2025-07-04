import pytest
from app import create_app
from app.database import Base, engine, SessionLocal
from app.database.models.player import Player


@pytest.fixture
def client():
    app = create_app()
    app.config.update({
        "TESTING": True
    })
    Base.metadata.create_all(bind=engine)

    with app.test_client() as client:
        yield app.test_client()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user1():
    db = SessionLocal()
    user = Player(username="testuser")
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    db.query(Player).filter_by(id=user.id).delete()
    db.commit()
    db.close()

@pytest.fixture
def test_user2():
    db = SessionLocal()
    user = Player(username="player2")
    db.add(user)
    db.commit()
    db.close()
    return user