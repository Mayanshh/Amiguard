from flask import Flask, request, jsonify, send_from_directory
import os
from dotenv import load_dotenv
import requests
from flask_cors import CORS

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend', static_url_path='/')
CORS(app)

# API config
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

# Serve frontend index
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Serve other frontend assets (CSS, JS, etc.)
@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

# Analyze toxicity
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    comment = data.get('comment', '')

    # Payload with spanAnnotations for word-level highlighting
    payload = {
        "comment": {"text": comment},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {
                "scoreType": "PROBABILITY",
                "scoreThreshold": 0.5
            },
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "THREAT": {},
            "PROFANITY": {},
            "IDENTITY_ATTACK": {}
        },
        "doNotStore": True,
        "spanAnnotations": True
    }

    # Send request to Perspective API
    response = requests.post(
        f"{PERSPECTIVE_URL}?key={PERSPECTIVE_API_KEY}",
        json=payload
    )

    return jsonify(response.json())

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
