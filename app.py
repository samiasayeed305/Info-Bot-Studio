from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder=".", template_folder=".")
CORS(app)

# ---------------- Watson Config ----------------
API_KEY = os.getenv("API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
SERVICE_URL = os.getenv("SERVICE_URL")
VERSION = os.getenv("VERSION", "2021-11-27")

# CORRECT V2 API URL (NO INSTANCE ID)
MESSAGE_URL = f"{SERVICE_URL}/v2/assistants/{ASSISTANT_ID}/message"

def send_to_watson(message):
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "input": {
            "message_type": "text",
            "text": message
        }
    }

    try:
        response = requests.post(
            MESSAGE_URL,
            params={"version": VERSION},
            headers=headers,
            auth=("apikey", API_KEY),
            json=payload
        )

        if response.status_code == 200:
            data = response.json()
            print("Watson Response:", data)

            responses = [
                item["text"]
                for item in data.get("output", {}).get("generic", [])
                if item.get("response_type") == "text"
            ]

            return "\n".join(responses) if responses else "I didn't understand that."

        else:
            return f"Error {response.status_code}: {response.text}"

    except Exception as e:
        return f"Exception: {str(e)}"

# ---------------- Routes ----------------
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/chatbot")
def chatbot():
    return send_from_directory(".", "chatbot.html")

@app.route("/api/message", methods=["POST"])
def message():
    user_msg = request.json.get("message", "").strip()
    if not user_msg:
        return jsonify({"reply": "Please type a message."})

    reply = send_to_watson(user_msg)
    return jsonify({"reply": reply})

@app.route("/test-config")
def test_config():
    result = send_to_watson("Hello")
    return jsonify({
        "test_message": "Hello",
        "response": result,
        "assistant_id": ASSISTANT_ID,
        "service_url": SERVICE_URL
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
