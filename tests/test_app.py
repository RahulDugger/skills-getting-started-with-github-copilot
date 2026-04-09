import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: (No setup needed, just use the client)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_for_activity():
    # Arrange
    email = "testuser1@mergington.edu"
    activity = "Chess Club"
    # Ensure user is not already signed up
    client.delete(f"/activities/{activity}/unregister?email={email}")

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json().get("message", "")
    # Clean up
    client.delete(f"/activities/{activity}/unregister?email={email}")

def test_signup_duplicate():
    # Arrange
    email = "testuser2@mergington.edu"
    activity = "Programming Class"
    client.delete(f"/activities/{activity}/unregister?email={email}")
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")
    # Clean up
    client.delete(f"/activities/{activity}/unregister?email={email}")

def test_unregister_participant():
    # Arrange
    email = "testuser3@mergington.edu"
    activity = "Gym Class"
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")

    # Assert
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json().get("message", "")

def test_unregister_nonexistent_participant():
    # Arrange
    email = "notregistered@mergington.edu"
    activity = "Chess Club"
    client.delete(f"/activities/{activity}/unregister?email={email}")

    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")

    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json().get("detail", "")

def test_signup_invalid_activity():
    # Arrange
    email = "testuser4@mergington.edu"
    activity = "Nonexistent Club"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json().get("detail", "")

def test_unregister_invalid_activity():
    # Arrange
    email = "testuser5@mergington.edu"
    activity = "Nonexistent Club"

    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json().get("detail", "")
