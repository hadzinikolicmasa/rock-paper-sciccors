from enum import Enum
from typing import Optional

import requests

class Choice(Enum):
    ROCK = (1, "rock")
    PAPER = (2, "paper")
    SCISSORS = (3, "scissors")
    LIZARD = (4, "lizard")
    SPOCK = (5, "spock")

    def __init__(self, id, label):
        self.id = id
        self.label = label

    @classmethod
    def get_by_id(cls, id: int) -> Optional["Choice"]:
        for choice in cls:
            if choice.id == id:
                return choice
        return None

    @classmethod
    def get_by_name(cls, name: str) -> Optional["Choice"]:
        for choice in cls:
            if choice.label == name:
                return choice
        return None

    @classmethod
    def get_choices(cls):
        return [{"id": c.id, "name": c.label} for c in cls]

    @classmethod
    def get_random_choice(cls):
        response = requests.get("https://codechallenge.boohma.com/random")
        number = response.json()["random_number"]
        choice_id = (number % 5) + 1
        return cls.get_by_id(choice_id)


WINNING_PAIRS = {
    (Choice.PAPER, Choice.ROCK),
    (Choice.PAPER, Choice.SPOCK),
    (Choice.ROCK, Choice.LIZARD),
    (Choice.ROCK, Choice.SCISSORS),
    (Choice.SCISSORS, Choice.PAPER),
    (Choice.SCISSORS, Choice.LIZARD),
    (Choice.LIZARD, Choice.PAPER),
    (Choice.LIZARD, Choice.SPOCK),
    (Choice.SPOCK, Choice.SCISSORS),
    (Choice.SPOCK, Choice.ROCK)
}


def get_result(player1: Choice, player2: Choice) -> str:
    if player1 == player2:
        return "tie"
    elif (player1, player2) in WINNING_PAIRS:
        return "win"
    else:
        return "lose"