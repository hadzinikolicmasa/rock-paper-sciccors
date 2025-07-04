import requests
from flask import Blueprint, request, jsonify
from app.database import SessionLocal
from app.database.models.player import Player
from app.database.models.match import Match
from app.services.game_logic import Choice, get_result


single_play_bp = Blueprint("single_play", __name__)


@single_play_bp.route("/play", methods=["POST"])
def single_play():
    data = request.get_json()
    username = data.get("username")
    choice_id = data.get("choice_id")

    if choice_id is None:
        return jsonify({"error": "You need to select a choice."}), 400

    player_choice = Choice.get_by_id(choice_id)
    if not player_choice:
        return jsonify({"error": "Invalid choice."}), 400

    try:
        res = requests.get("https://codechallenge.boohma.com/random")
        number = res.json()["random_number"]
        computer_choice = Choice.get_by_id((number % 5) + 1)
    except Exception:
        return jsonify({"error": "Failed to get random number"}), 500

    result = get_result(player_choice, computer_choice)

    if username:
        db = SessionLocal()
        player = db.query(Player).filter_by(username=username).first()

        if not player:
            db.close()
            return jsonify({"error": "User not found."}), 404

        winner_id = None

        if result == "win":
            winner_id = player.id
        elif result == "lose":
            winner_id = -1

        match = Match(
            player1_id=player.id,
            player2_id=None,
            player1_choice=player_choice.label,
            player2_choice=computer_choice.label,
            winner_id=winner_id,
            completed=True
        )

        db.add(match)
        db.commit()
        db.close()

    return jsonify({
        "result": result,
        "player_choice": {
            "id": player_choice.id,
            "name": player_choice.label
        },
        "computer_choice": {
            "id": computer_choice.id,
            "name": computer_choice.label
        }
    })
