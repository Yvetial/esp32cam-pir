from flask import Flask, request, jsonify, send_file, render_template
import os
import base64
from datetime import datetime
import glob


app = Flask(__name__)

UPLOAD_FOLDER = "snapshots"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store device statuses (hanya untuk buzzer)
device_status = {
    "buzzer": "off"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_snapshot():
    data = request.get_json()
    image_base64 = data.get("image")

    if not image_base64:
        return jsonify({"status": "error", "message": "No image received"}), 400

    try:
        image_bytes = base64.b64decode(image_base64)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{timestamp}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        with open(filepath, "wb") as f:
            f.write(image_bytes)

        return jsonify({"status": "success", "filename": filename}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/snapshot_latest")
def snapshot_latest():
    files = sorted(glob.glob(os.path.join(UPLOAD_FOLDER, "*.jpg")), reverse=True)
    if not files:
        return "No snapshot available", 404
    return send_file(files[0], mimetype="image/jpeg")

@app.route("/device/buzzer", methods=["GET", "POST"])
def control_buzzer():
    if request.method == "POST":
        data = request.get_json()
        status = data.get("status")
        if status not in ["on", "off"]:
            return jsonify({"status": "error", "message": "Invalid status"}), 400
        device_status["buzzer"] = status
        return jsonify({"status": "success", "device": "buzzer", "new_status": status})

    # GET method returns current buzzer status
    return jsonify({"device": "buzzer", "status": device_status["buzzer"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

def handler(environ, start_response):
    return app(environ, start_response)