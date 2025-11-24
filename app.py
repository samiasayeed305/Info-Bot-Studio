from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

# ----------------------------- IBM Watson Config -----------------------------
API_KEY = "et2erlTLLSh4Y-el2mRsJJhu4ytgJqj2cMT0kXNDZ7k4"          # Replace with your API Key
SERVICE_URL = "https://api.au-syd.assistant.watson.cloud.ibm.com/instances/33fd5ad8-9b47-4897-bad7-8df517087d7f"  # Replace with your Service URL (e.g., https://api.au-syd.assistant.watson.cloud.ibm.com)
ASSISTANT_ID = "49ac90f4-a470-4f41-941b-55c5c1eeed0c"  # Replace with your Assistant ID

# Watson Assistant v2 API URL
URL = f"{SERVICE_URL}/v2/assistants/{ASSISTANT_ID}/message?version=2025-11-24"

# ----------------------------- Frontend Route -----------------------------
@app.route('/')
def index():
    return send_from_directory('.', 'chatbot.html')  # Serve your HTML file

# ----------------------------- Backend Route -----------------------------
@app.route("/api/message", methods=["POST"])
def message():
    user_msg = request.json.get("message", "").strip()
    if not user_msg:
        return jsonify({"reply": "Please type a message."})

    payload = {
        "input": {
            "message_type": "text",
            "text": user_msg
        }
    }

    try:
        # Send request to Watson Assistant with basic auth
        response = requests.post(
            URL,
            json=payload,
            auth=HTTPBasicAuth('apikey', API_KEY),
            timeout=10
        )
        response.raise_for_status()
        result = response.json()

        # Extract all text responses from Watson
        generic_responses = result.get("output", {}).get("generic", [])
        reply_texts = [g.get("text") for g in generic_responses if g.get("text")]
        reply = "\n".join(reply_texts) if reply_texts else "No response from Watson."

    except requests.exceptions.HTTPError as e:
        reply = f"HTTP error: {str(e)}"
    except requests.exceptions.ConnectionError:
        reply = "Connection error: Cannot reach Watson Assistant."
    except requests.exceptions.Timeout:
        reply = "Request timed out. Please try again."
    except Exception as e:
        reply = f"Unexpected error: {str(e)}"

    return jsonify({"reply": reply})

# ----------------------------- Run Flask -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
