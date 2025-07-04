# Rock-Paper-Scissors-Lizard-Spock Game

This app  allows players to play Rock-Paper-Scissors-Lizard-Spock against the computer (single-player) or against another player (multiplayer). The backend is built with Flask, and the frontend is built with Vue.js . The entire application is containerized using Docker for consistent local development and deployment.

---

## Prerequisites

Before running this application, ensure the following tools are installed:

- **Docker** and **python**
- **Node.js** and **Vue CLI**


## How to Run the Application (with Docker)

```bash
docker compose up --build
```

## Running Backend Tests Locally

First make virtual env and install the requirements :

For Linux/MacOS
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

or Windows

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```


Run all test files:
```bash
pytest
```

or run a specific test :
```bash
pytest tests/test_choices.py
```

## How the App Works – Rock-Paper-Scissors-Lizard-Spock
This application allows users to play the extended version of Rock-Paper-Scissors either:

- Single-player – against the computer

- Multiplayer – against another real user

### Single-Player Mode
The user enters their username (optional).

They select a move: rock, paper, scissors, lizard, or spock.

The backend randomly selects a move for the computer.

The winner is calculated based on the rules.

The result is shown to the player.

If a username is provided, the result is stored in the database.

Additional features:
Users can view their last 10 game results.

Users can delete their history using the DELETE /results/reset endpoint.

### Multiplayer Mode
**Phase 1:** Player One starts a match
Player One chooses a move and sends a request without match_id.

A new match is created on the backend with status "waiting".

The backend responds with a match_id.

**Phase 2:** Waiting for Player Two
The app waits up to 10 seconds for another player to join.

The frontend uses polling to see if the match is complete and if the other user played the move (better implementation would be with Sockets but for this small project polling works too).

If Player Two doesn't join within 10 seconds, the match is closed.

or **Phase 3:** Player Two joins
Player Two submits a move with the match_id.

The backend updates the match, determines the winner, and marks it as "done".

The result is sent back and displayed to both players.
