from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Simulasi status device (buzzer)
device_status = {
    "buzzer": "off"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_snapshot():
    # Simulasi upload snapshot tanpa menyimpan file
    data = request.get_json()
    image_base64 = data.get("image")

    if not image_base64:
        return jsonify({"status": "error", "message": "No image received"}), 400

    return jsonify({"status": "success", "message": "Simulasi upload sukses"}), 200

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

# Handler untuk Vercel (serverless)
def handler(environ, start_response):
    return app(environ, start_response)
