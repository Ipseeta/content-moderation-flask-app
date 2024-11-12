This is a RESTful API built with Flask, designed to perform content moderation using OpenAI's API. The API is deployed on Vercel and can be accessed remotely. This project uses pydantic for data validation and python-dotenv for environment variable management.

<h1>Features</h1>
<b>Content Moderation</b>: Uses OpenAI's GPT model to analyze content for harmful or inappropriate material.
<b>Vercel Deployment</b>: Hosted on Vercel for easy access and scalability.
<b>Data Validation</b>: Ensures structured JSON output using pydantic.

1. Running Locally
without vercel run

``flask run``
Access at http://127.0.0.1:5000

2. Deployment on Vercel
Install the Vercel CLI:

``npm install -g vercel``
Log in to Vercel:

``vercel login``

Deploy the project:

``vercel``

Vercel will generate a public URL where the API is accessible.

3. Testing:

curl -X POST "https://your-vercel-deployment-url/api/analyze_content" \
  -H "Content-Type: application/json" \
  -d '{
        "content": "Your text to analyze",
        "type": "harrassment"
      }'

Postman Post request to test
https://content-moderation-flask-app.vercel.app/analyze_content

Content-Type : "application/json"
{
	"content": "This message suggests actions that could lead to physical harm if followed.",
 	"type": "sexual content"
}


4. API Endpoints
POST /analyze_content
Analyze content for harmful or inappropriate material.

Request Body

Parameter	Type	Description
content	string	The text content to analyze.
type	string	The type of content (e.g., "sexual content", "harrassment").

Response
The API returns a JSON object containing flagged categories and confidence scores for each category.

Example Response:

json

{
  "content": "Your text to analyze",
  "type": "sexual content",
  "flagged_categories": {
    "violence": 0.8,
    "hate_speech": 0.6
  },
  "confidence_scores": {
    "violence": 0.8,
    "sexual_content": 0.2,
    "hate_speech": 0.6,
    "self_harm": 0.1,
    "harassment": 0.3,
    "illicit_activities": 0.2,
    "suggestive_language": 0.4
  }
}
Environment Variables
Configure these environment variables in a .env file for local development and in Vercel’s dashboard for deployment:

Variable	Description
OPENAI_API_KEY	Your OpenAI API key.