import os
from flask import Flask, request, jsonify, send_file
from google import genai
from dotenv import load_dotenv

# Load your .env file
load_dotenv()

app = Flask(__name__)

# Setup the Client (This is the new correct syntax)
google_api_key = os.environ.get("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY not set in environment or .env file")

client = genai.Client(api_key=google_api_key)

# Define the Persona
instruction = (
    "You are MediGuide, a professional medical information assistant. "
    "Provide clear, evidence-based health information to the user. "
    "IMPORTANT: Always include a disclaimer that you are an AI, not a doctor, "
    "and that users should seek professional medical advice for emergencies."
)

# This serves your index.html file without needing a 'templates' folder
@app.route('/')
def index():
    return send_file('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # 1. Safely grab the data
    user_data = request.get_json()
    if not user_data or "message" not in user_data:
        return jsonify({"error": "No message received"}), 400

    user_message = user_data.get("message")
    print(f"User sent: {user_message}") # This will show in your terminal

    try:
        # 2. Use the exact SDK structure
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_message, # The SDK usually handles strings directly
            config={
                "system_instruction": instruction,
                "temperature": 0.3
            }
        )
        
        # 3. Handle empty responses
        ai_text = response.text if response.text else "I'm sorry, I couldn't generate a response."
        return jsonify({"response": ai_text})
        
    except Exception as e:
        print(f"AI Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)