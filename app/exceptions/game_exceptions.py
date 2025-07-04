from enum import Enum

class GameException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

class ErrorMessages(Enum):
    WRONG_OPPONENT_PLAYER = ("You can't play against yourself.", 400)
    MATCH_ALREADY_COMPLETED = ("Match is already completed.", 400)

