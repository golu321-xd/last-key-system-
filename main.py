from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)

# Key storage
keys = {}

@app.route("/")
def home():
    return "Rayfield Key System Working!"

@app.route("/key")
def generate_key():
    generated_key = str(uuid.uuid4())

    keys[generated_key] = {
        "expires": datetime.utcnow() + timedelta(hours=48)  # 48 hours validity
    }

    return jsonify({
        "status": "success",
        "key": generated_key,
        "expires_in": "48 hours"
    })

@app.route("/validate", methods=["GET"])
def validate_key():
    key = request.args.get("key")

    if key not in keys:
        return jsonify({"valid": False, "msg": "Key not found"}), 404

    if datetime.utcnow() > keys[key]["expires"]:
        return jsonify({"valid": False, "msg": "Key expired"}), 403

    return jsonify({"valid": True, "msg": "Key valid"}), 200
