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
