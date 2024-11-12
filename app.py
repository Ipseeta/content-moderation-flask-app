from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError, Field
import os
import json

load_dotenv()

app = Flask(__name__)

# Set up the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the expected response schema using pydantic
class ModerationScores(BaseModel):
    violence: float = Field(..., ge=0.0, le=1.0)
    sexual_content: float = Field(..., ge=0.0, le=1.0)
    hate_speech: float = Field(..., ge=0.0, le=1.0)
    self_harm: float = Field(..., ge=0.0, le=1.0)
    harassment: float = Field(..., ge=0.0, le=1.0)
    illicit_activities: float = Field(..., ge=0.0, le=1.0)
    suggestive_language: float = Field(..., ge=0.0, le=1.0)

@app.route('/analyze_content', methods=['POST'])
def analyze_content():
    data = request.json

    # Validate input
    content = data.get("content")
    content_type = data.get("type")
    
    if not content:
        return jsonify({"error": "Content is required"}), 400
    if not content_type:
        return jsonify({"error": "Content type is required"}), 400


    try:
        # Use OpenAI's chat model to analyze the content with client instance
        response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",  # Specify the chat model
            messages=[
                {
                    "role": "system",
                    "content":f"""
                    You are a content moderation assistant. Analyze the user content for the presence of {content_type}. 
                    Assess each category on a scale from 0 to 1 (0 meaning no risk, 1 meaning high risk). Only respond with a JSON object containing the categories and their respective scores.
                    IMPORTANT: Respond ONLY with valid JSON in this exact format. Do not include any extra explanations, just the JSON object.
            
                    Categories to evaluate:
                    - violence
                    - sexual content
                    - hate speech
                    - self-harm
                    - harassment
                    - illicit activities
                    - suggestive language
                    
                    Respond in this format:
                    {{
                        "violence": <score>,
                        "sexual_content": <score>,
                        "hate_speech": <score>,
                        "self_harm": <score>,
                        "harassment": <score>,
                        "illicit_activities": <score>,
                        "suggestive_language": <score>
                    }}
                """
                }, 
                {
                    "role": "user", "content": content
                }
            ],
            max_tokens=150,
            temperature=0.3,
            top_p=1,
            n=1
        )

        # Extract JSON response from the model output
        moderation_result = response.choices[0].message.content.strip()

        # Validate and parse the JSON output with Pydantic
        try:
            scores = ModerationScores.parse_raw(moderation_result)
        except ValidationError as e:
            return jsonify({"error": "Invalid response format", "details": e.errors()}), 500

        # Set a threshold to flag categories
        threshold = 0.5
        flagged_categories = {category: score for category, score in scores.dict().items() if score > threshold}

        # Return the results
        output = {
            "content": content,
            "type": content_type,
            "flagged_categories": flagged_categories,
            "confidence_scores": scores.dict()
        }

        return jsonify(output)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
