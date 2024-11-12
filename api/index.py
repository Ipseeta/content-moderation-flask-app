from app import app  # Import your Flask app from app.py

# Vercel will use this as the entry point
app.config["SERVER_NAME"] = "localhost"  # Workaround for local host settings if needed
