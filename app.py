from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)
KEYS_FILE = "keys.json"

def load_keys():
    try:
        with open(KEYS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_keys(data):
    with open(KEYS_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/add_key", methods=["POST"])
def add_key():
    data = request.json
    key = data["key"]
    user_id = data["user_id"]
    expires = data["expires"]

    keys = load_keys()
    keys[key] = {"user_id": user_id, "expires": expires}
    save_keys(keys)
    return jsonify({"status": "ok"})

@app.route("/check_key")
def check_key():
    key = request.args.get("key")
    keys = load_keys()

    if key in keys:
        expires = datetime.fromisoformat(keys[key]["expires"])
        now = datetime.utcnow()
        return jsonify({
            "valid": expires > now,
            "expires": keys[key]["expires"]
        })
    else:
        return jsonify({"valid": False})

if __name__ == "__main__":
    app.run(debug=True)
