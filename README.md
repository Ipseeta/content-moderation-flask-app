This is a RESTful API built with Flask, designed to perform content moderation using OpenAI's API. The API is deployed on Vercel and can be accessed remotely. This project uses pydantic for data validation and python-dotenv for environment variable management.

## Features

- **Content Moderation**: Uses OpenAI's GPT model to analyze content for harmful or inappropriate material.
- **Vercel Deployment**: Hosted on Vercel for easy access and scalability.
- **Data Validation**: Ensures structured JSON output using `pydantic`.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   
2. Install Dependencies
   ```bash
   pip install -r requirements.txt

3. Set up environment variables by creating a ``.env file`` in the project root 

## Testing

1. To test the API locally:

Run the Flask app with the following command:

```export FLASK_APP=api.index flask run```

Access the API at http://127.0.0.1:5000

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

## API Endpoints
POST /analyze_content
Analyze content for harmful or inappropriate material.

Request Body
### Request Body

The request body should be in JSON format and include the following parameters:

| Parameter   | Type   | Required | Description                                 |
|-------------|--------|----------|---------------------------------------------|
| `content`   | string | Yes      | The text content to analyze for moderation. |
| `type`      | string | Yes      | The type of content (e.g., "harrassment").         |

#### Example Request Body

```json
{
  "content": "This is an example text to analyze.",
  "type": "harrassment"
}
```
### Response

The API returns a JSON object containing the analyzed content, flagged categories, and confidence scores for each category.

#### Example Response

```json
{
  "content": "This is an example text to analyze.",
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
```
Environment Variables
Configure these environment variables in a ```.env``` file for local development and in Vercel’s dashboard for deployment:
| Variable   | Description   |
|-------------|--------|
|OPENAI_API_KEY|	Your OpenAI API key|.
