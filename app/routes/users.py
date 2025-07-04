from flask import Blueprint, request, jsonify
from app.database import SessionLocal
from app.database.models.player import Player

users_bp = Blueprint("users", __name__)

@users_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username required"}), 400

    db = SessionLocal()
    existing = db.query(Player).filter_by(username=username).first()

    if existing:
        db.close()
        return jsonify({"error": "Username already exists"}), 409

    new_user = Player(username=username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return jsonify({"message": "User registered", "user_id": new_user.id})
