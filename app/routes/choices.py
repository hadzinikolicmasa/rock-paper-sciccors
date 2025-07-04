from flask import Blueprint, jsonify
from app.services.game_logic import Choice

choices_bp = Blueprint("choices", __name__)

@choices_bp.route("/choices", methods=["GET"])
def get_choices():
    return jsonify(Choice.get_choices())


@choices_bp.route("/choice", methods=["GET"])
def get_choice():
    random_choice = Choice.get_random_choice()
    return jsonify({"id": random_choice.id, "name": random_choice.label})