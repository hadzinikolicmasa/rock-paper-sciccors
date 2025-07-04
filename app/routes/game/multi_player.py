from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from app.database import SessionLocal
from app.database.models.player import Player
from app.database.models.match import Match
from app.exceptions.game_exceptions import GameException, ErrorMessages
from app.services.game_logic import Choice, get_result

multi_play_bp = Blueprint("multi_play", __name__)

@multi_play_bp.route("/multi/play", methods=["POST"])
def multi_play():
    data = request.get_json()
    username = data.get("username")
    choice_id = data.get("choice_id")
    match_id = data.get("match_id")

    if not username or choice_id is None:
        return jsonify({"error": "Username and choice are required."}), 400

    db = SessionLocal()

    player = db.query(Player).filter_by(username=username).first()
    if not player:
        db.close()
        return jsonify({"error": "User not found."}), 404

    player_choice = Choice.get_by_id(choice_id)
    if not player_choice:
        db.close()
        return jsonify({"error": "Invalid choice."}), 400


    if not match_id:
        new_match = Match(
            player1_id=player.id,
            player1_choice=player_choice.label,
            completed=False
        )
        db.add(new_match)
        db.commit()
        db.refresh(new_match)
        db.close()

        return jsonify({
            "message": "Match created. Share match_id with opponent.",
            "match_id": new_match.id
        })

    match = (
        db.query(Match)
        .options(joinedload(Match.player1))
        .filter_by(id=match_id)
        .first()
    )

    if not match:
        db.close()
        return jsonify({"error": "Match not found"}), 404

    if match.completed:
        db.close()
        raise GameException(*ErrorMessages.MATCH_ALREADY_COMPLETED.value)

    if match.player1_id == player.id:
        db.close()
        raise GameException(*ErrorMessages.WRONG_OPPONENT_PLAYER.value)

    match.player2_id = player.id
    match.player2_choice = player_choice.label

    p1 = Choice.get_by_name(match.player1_choice)
    p2 = Choice.get_by_name(match.player2_choice)

    result = get_result(p2, p1)

    if result == "win":
        match.winner_id = player.id
        winner_name = player.username
    elif result == "lose":
        match.winner_id = match.player1_id
        winner_name = match.player1.username
    else:
        match.winner_id = None
        winner_name = "Tie"

    match.completed = True

    player1_username = match.player1.username
    player2_username = player.username

    player1_choice = match.player1_choice
    player2_choice = player_choice.label

    db.commit()
    db.close()

    return jsonify({
        "message": "Match completed!",
        "player_one": {
            "username": player1_username,
            "choice": player1_choice,
        },
        "player_two": {
            "username": player2_username,
            "choice": player2_choice,
        },
        "winner": winner_name
    })


@multi_play_bp.route("/multi/status", methods=["GET"])
def get_match_status():
    match_id = request.args.get("match_id")

    db = SessionLocal()
    match = db.query(Match).filter_by(id=match_id).first()

    if not match:
        db.close()
        return jsonify({"error": "Match not found"}), 404

    if not match.completed and datetime.utcnow() - match.created_at > timedelta(seconds=10):
        db.delete(match)
        db.commit()
        db.close()
        return jsonify({
            "status": "expired",
            "message": "Match expired due to inactivity."
        })

    if not match.completed:
        db.close()
        return jsonify({"status": "waiting"})

    result = {
        "status": "done",
        "player_one": {
            "username": match.player1.username,
            "choice": match.player1_choice,
        },
        "player_two": {
            "username": match.player2.username,
            "choice": match.player2_choice,
        },
        "winner": match.winner.username
    }

    db.close()
    return jsonify(result)
