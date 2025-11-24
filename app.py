from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# -----------------------------
# UPDATE THESE VARIABLES
# -----------------------------
API_KEY = "yP5WQmNTzLgC_dWHsOnBQMH2r9ekTM2uw237J5AvsFWs"                    # Copy your API Key from IBM Cloud
SERVICE_URL = "https://api.au-syd.assistant.watson.cloud.ibm.com/instances/33fd5ad8-9b47-4897-bad7-8df517087d7f"   # Example: https://api.us-south.assistant.watson.cloud.ibm.com
LIVE_ENV_ID = "31e141fd-6547-4e23-9a2b-54c23732da42"   # From Deploy → Live Environment ID

# Full endpoint for sending messages
URL = f"{SERVICE_URL}/v2/assistants/{LIVE_ENV_ID}/message"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

@app.route("/api/message", methods=["POST"])
def message():
    user_msg = request.json.get("message", "")
    
    # Prepare payload in new Watsonx format
    payload = {
        "input": {
            "message_type": "text",
            "text": user_msg
        }
    }

    try:
        response = requests.post(URL, json=payload, headers=headers)
        result = response.json()
        # Extract reply safely
        reply = result.get("output", [{}])[0].get("generic", [{}])[0].get("text", "No response")
    except Exception as e:
        reply = f"Error: {str(e)}"

    return jsonify({"reply": reply})


if __name__ == "__main__":
    # Run locally on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
