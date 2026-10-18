from flask import Flask, request, jsonify
import joblib
import pandas as pd

from app.backend.LungCancerPrediction import predict

app = Flask(__name__)

# Load model file
data = joblib.load('LungCancer_classifier_and_features.pickle')

# Unpack classifier and required feature column names
model = data['classifier']
expected_features = data['features']


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "expected_features": list(expected_features)
    }), 200



@app.route("/predict", methods=["POST"])
def prediction_endpoint():
    try:
        payload = request.get_json(silent=True)
        if not payload or "filepath" not in payload:
            return jsonify({"detail": "Missing required field 'filepath' in request body."}), 400

        filepath = payload["filepath"]

        results = predict(filepath)

        return jsonify({
            "status": "success",
            "predictions": results
        }), 200

    except FileNotFoundError as e:
        return jsonify({"detail": str(e)}), 404

    except Exception as e:
        return jsonify({"detail": str(e)}), 500
