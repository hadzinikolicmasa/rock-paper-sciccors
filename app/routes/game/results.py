from flask import Blueprint, jsonify, request
from app.database import SessionLocal
from app.database.models.player import Player
from app.database.models.match import Match

results_bp = Blueprint("results", __name__)

@results_bp.route("/results", methods=["POST"])
def get_latest_results():
    data = request.get_json()
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    db = SessionLocal()
    player = db.query(Player).filter(Player.username == username).first()

    if not player:
        return jsonify({"error": "Player not found"}), 404

    matches = (
        db.query(Match)
        .filter(
            (Match.player1_id == player.id) | (Match.player2_id == player.id),
            Match.completed == True
        )
        .order_by(Match.id.desc())
        .limit(10)
        .all()
    )

    results = []
    for match in matches:
        is_player_one = match.player1_id == player.id

        your_choice = match.player1_choice if is_player_one else match.player2_choice
        opponent_choice = match.player2_choice if is_player_one else match.player1_choice

        opponent = (
            match.player2.username if is_player_one and match.player2
            else match.player1.username if not is_player_one and match.player1
            else "Computer"
        )

        if match.winner_id is None:
            result = "tie"
        elif match.winner_id == player.id:
            result = "win"
        else:
            result = "lose"

        results.append({
            "opponent": opponent,
            "your_choice": your_choice,
            "opponent_choice": opponent_choice,
            "result": result
        })

    db.close()
    return jsonify(results)


@results_bp.route("/results/reset", methods=["DELETE"])
def reset_user_results():
    data = request.get_json()
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    db = SessionLocal()
    player = db.query(Player).filter_by(username=username).first()

    if not player:
        db.close()
        return jsonify({"error": "User not found"}), 404

    db.query(Match).filter(Match.player1_id == player.id).delete()
    db.query(Match).filter(Match.player2_id == player.id).delete()

    db.commit()
    db.close()

    return jsonify({"message": f"Results cleared!"})
