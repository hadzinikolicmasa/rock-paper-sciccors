from flask import Flask
from app.routes.game.multi_player import multi_play_bp
from app.routes.game.results import results_bp
from app.routes.game.single_player import single_play_bp
from app.routes.users import users_bp
from app.routes.choices import choices_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(choices_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(single_play_bp)
    app.register_blueprint(results_bp)
    app.register_blueprint(multi_play_bp)

    return app
