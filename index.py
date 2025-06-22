from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS
import base64
import time

app = Flask(__name__, template_folder="templates")
CORS(app)

last_snapshot_base64 = None
last_snapshot_time = 0
device_status = {
    "buzzer": "off"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_snapshot():
    global last_snapshot_base64, last_snapshot_time
    data = request.get_json()
    image_base64 = data.get("image")

    if not image_base64:
        return jsonify({"status": "error", "message": "No image received"}), 400

    last_snapshot_base64 = image_base64 
    last_snapshot_time = time.time()
    return jsonify({"status": "success", "message": "Snapshot diterima"}), 200

@app.route("/snapshot_latest")
def snapshot_latest():
    if not last_snapshot_base64:
        return "No snapshot available", 404

    image_bytes = base64.b64decode(last_snapshot_base64)
    return Response(image_bytes, mimetype='image/jpeg')

@app.route("/device/buzzer", methods=["GET", "POST"])
def control_buzzer():
    if request.method == "POST":
        data = request.get_json()
        status = data.get("status")
        if status not in ["on", "off"]:
            return jsonify({"status": "error", "message": "Invalid status"}), 400
        device_status["buzzer"] = status
        return jsonify({"status": "success", "device": "buzzer", "new_status": status})

    return jsonify({"device": "buzzer", "status": device_status["buzzer"]})

@app.route("/device/camera")
def camera_status():
    return jsonify({"status": "online"})

@app.route("/snapshot_status")
def snapshot_status():
    global last_snapshot_time
    current_time = time.time()
    elapsed = current_time - last_snapshot_time
    if elapsed > 10:
        return jsonify({"status": "old"}) 
    return jsonify({"status": "fresh"})  
