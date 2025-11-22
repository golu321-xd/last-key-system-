from flask import Flask, request, jsonify
import json, time, uuid, os

app = Flask(__name__)

FILE = "keys.json"

def load():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)

def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/generate", methods=["POST"])
def generate():
    data = load()
    player = request.json.get("player_id")

    if player in data and data[player]["expires"] > time.time():
        return jsonify({"key": data[player]["key"]})

    new = str(uuid.uuid4())
    expires = time.time() + 48 * 3600

    data[player] = {"key": new, "expires": expires}
    save(data)

    return jsonify({"key": new})

@app.route("/verify", methods=["POST"])
def verify():
    data = load()
    player = request.json.get("player_id")
    key = request.json.get("key")

    if player not in data:
        return jsonify({"success": False, "msg": "Key not generated"})

    saved = data[player]

    if saved["key"] != key:
        return jsonify({"success": False, "msg": "Wrong key"})

    if saved["expires"] < time.time():
        return jsonify({"success": False, "msg": "Key expired"})

    return jsonify({"success": True})
