import pytest
from app.database import SessionLocal
from app.database.models.match import Match
from app.database.models.player import Player
from app.exceptions.game_exceptions import GameException


@pytest.fixture
def player1():
    db = SessionLocal()
    user = Player(username="player1")
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    db.query(Player).filter_by(id=user.id).delete()
    db.commit()
    db.close()


@pytest.fixture
def player2():
    db = SessionLocal()
    user = Player(username="player2")
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    db.query(Player).filter_by(id=user.id).delete()
    db.commit()
    db.close()


@pytest.fixture
def test_match(player1):
    db = SessionLocal()
    match = Match(
        player1_id=player1.id,
        player1_choice="rock",
        completed=True
    )
    db.add(match)
    db.commit()
    db.refresh(match)
    yield match
    db.query(Match).filter_by(id=match.id).delete()
    db.commit()
    db.close()


def test_create_multiplayer_match(client, player1):
    res = client.post("/multi/play", json={
        "username": player1.username,
        "choice_id": 1
    })

    assert res.status_code == 200
    data = res.get_json()
    assert "match_id" in data
    assert data["message"] == "Match created. Share match_id with opponent."


def test_join_and_complete_match(client, player1, player2):
    create_res = client.post("/multi/play", json={
        "username": player1.username,
        "choice_id": 1
    })
    match_id = create_res.get_json()["match_id"]

    res = client.post("/multi/play", json={
        "username": player2.username,
        "choice_id": 2,
        "match_id": match_id
    })

    assert res.status_code == 200
    data = res.get_json()
    assert data["message"] == "Match completed!"
    assert "winner" in data


def test_play_against_self_raises(client, player1):
    res1 = client.post("/multi/play", json={
        "username": player1.username,
        "choice_id": 1
    })
    match_id = res1.get_json()["match_id"]

    with pytest.raises(GameException) as exc_info:
        client.post("/multi/play", json={
            "username": player1.username,
            "choice_id": 2,
            "match_id": match_id
        })

    assert str(exc_info.value.message) == "You can't play against yourself."


def test_join_invalid_match(client, player2):
    res = client.post("/multi/play", json={
        "username": player2.username,
        "choice_id": 2,
        "match_id": 99999
    })

    assert res.status_code == 404
    data = res.get_json()
    assert data["error"] == "Match not found"


