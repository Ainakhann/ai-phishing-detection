"""
app.py — DarkByte Flask API
Imports shared detection logic from detector.py
Team DarkByte | K.R. Mangalam University | B.Tech Minor Project
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from detector import analyze_url, analyze_email
import os

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def index():
    """Serve the frontend HTML file."""
    return send_from_directory(os.path.dirname(__file__), "index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    content_type = data.get("type", "").lower()
    content = data.get("content", "").strip()

    if not content:
        return jsonify({"error": "Content cannot be empty"}), 400

    if content_type == "url":
        result = analyze_url(content)
    elif content_type == "email":
        result = analyze_email(content)
    else:
        return jsonify({"error": "type must be 'url' or 'email'"}), 400

    return jsonify(result), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "online", "team": "DarkByte", "version": "1.0.0"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
