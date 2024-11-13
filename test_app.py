import pytest
from flask import Flask, jsonify
from api.index import app
from pydantic import ValidationError

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test cases

def test_home_route(client):
    """Test the home route for a successful response"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"Hello, World!"

def test_analyze_content_missing_content(client):
    """Test analyze_content endpoint with missing content"""
    response = client.post("/analyze_content", json={"type": "text"})
    data = response.get_json()
    assert response.status_code == 400
    assert data["error"] == "Content is required"

def test_analyze_content_missing_type(client):
    """Test analyze_content endpoint with missing type"""
    response = client.post("/analyze_content", json={"content": "Test content"})
    data = response.get_json()
    assert response.status_code == 400
    assert data["error"] == "Content type is required"

def test_analyze_content_valid_request(client, mocker):
    """Test analyze_content endpoint with a valid request and mock OpenAI response"""
    mock_response = {
        "choices": [
            {
                "message": {
                    "content": '{"violence": 0.4, "sexual_content": 0.1, "hate_speech": 0.2, "self_harm": 0.1, "harassment": 0.3, "illicit_activities": 0.0, "suggestive_language": 0.2}'
                }
            }
        ]
    }

    # Mock the OpenAI API response
    mocker.patch("openai.ChatCompletion.create", return_value=mock_response)
    
    response = client.post(
        "/analyze_content",
        json={"content": "This is a violence content.", "type": "violence"}
    )
    data = response.get_json()

    assert response.status_code == 200
    assert "confidence_scores" in data
    assert "flagged_categories" in data

def test_invalid_response_format(client, mocker):
    """Test analyze_content endpoint with an invalid OpenAI response format"""

    # Mock ModerationScores.model_validate_json to raise a ValueError (simulating a parsing failure)
    mocker.patch("api.index.ModerationScores.model_validate_json", side_effect=ValueError("Invalid JSON format"))

    # Make the request to the analyze_content endpoint
    response = client.post(
        "/analyze_content",
        json={"content": "This is a test content.", "type": "text"}
    )
    data = response.get_json()

    # Validate the response status and content
    assert response.status_code == 500
    assert "error" in data
    assert "Invalid response format" in data["error"]