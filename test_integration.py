import requests

BASE_URL = "https://content-moderation-flask-app.vercel.app"  # Replace with your Vercel deployment URL

def test_vercel_home():
    """Test the home route of the deployed app"""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.text == "Hello, World!"

def test_vercel_analyze_content_valid_request():
    """Test the analyze_content endpoint on Vercel with a valid request"""
    response = requests.post(
        f"{BASE_URL}/analyze_content",
        json={"content": "This is an example sexual text to analyze.", "type": "sexual"}
    )
    data = response.json()

    assert response.status_code == 200
    assert "confidence_scores" in data
    assert "flagged_categories" in data
    assert isinstance(data["confidence_scores"], dict)

def test_vercel_analyze_content_missing_content():
    """Test the analyze_content endpoint on Vercel with missing content"""
    response = requests.post(
        f"{BASE_URL}/analyze_content",
        json={"type": "harrassment"}
    )
    data = response.json()

    assert response.status_code == 400
    assert data["error"] == "Content is required"

def test_vercel_analyze_content_invalid_response_format():
    """Test the analyze_content endpoint on Vercel with invalid format in OpenAI response"""
    response = requests.post(
        f"{BASE_URL}/analyze_content",
        json={"content": "Invalid content", "type": "invalid"}
    )

    assert response.status_code in [200, 500]  # Expect a valid response or an error handling code
