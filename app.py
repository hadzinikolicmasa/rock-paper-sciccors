from flask import jsonify
from app import create_app
from app.database import Base, engine
from app.exceptions.game_exceptions import GameException

app = create_app()
Base.metadata.create_all(bind=engine)

@app.errorhandler(GameException)
def handle_game_exception(error):
    return jsonify({"error": error.message}), error.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    print("Registered routes:")
    print(app.url_map)

