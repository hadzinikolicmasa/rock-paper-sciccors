def test_get_choices(client):
    response = client.get("/choices")
    data = response.get_json()

    assert response.status_code == 200

    mock_choices = {"rock", "paper", "scissors", "lizard", "spock"}
    returned_names = {item["name"] for item in data}
    assert returned_names == mock_choices

    mock_ids = {1, 2, 3, 4, 5}
    returned_ids = {item["id"] for item in data}
    assert returned_ids == mock_ids


def test_random_choices(client):
    response = client.get("/choice")
    data = response.get_json()

    assert response.status_code == 200

    choice_id = data["id"]
    choice_name = data["name"]

    assert choice_name in ["rock", "paper", "scissors", "lizard", "spock"]
    assert choice_id in [1, 2, 3, 4, 5]
