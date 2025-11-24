from flask import Flask, request, jsonify
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------------------------
# ADD YOUR WATSON CREDENTIALS
# ---------------------------
API_KEY = "xrvJw9IqRSuM2ucbQ6ac2otoBwGFfmNlWmQ7omKhg0Tb"
ASSISTANT_ID = "49ac90f4-a470-4f41-941b-55c5c1eeed0c"
URL = "https://api.au-syd.assistant.watson.cloud.ibm.com/instances/33fd5ad8-9b47-4897-bad7-8df517087d7f"

auth = IAMAuthenticator(API_KEY)
assistant = AssistantV2(
    version="2021-06-14",
    authenticator=auth
)
assistant.set_service_url(URL)

# Create session
session = assistant.create_session(assistant_id=ASSISTANT_ID).get_result()

@app.route("/api/message", methods=["POST"])
def message():
    user_msg = request.json["message"]

    response = assistant.message(
        assistant_id=ASSISTANT_ID,
        session_id=session["session_id"],
        input={
            "message_type": "text",
            "text": user_msg
        }
    ).get_result()

    reply = response["output"]["generic"][0]["text"]

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
