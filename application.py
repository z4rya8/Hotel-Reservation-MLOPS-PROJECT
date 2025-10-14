import joblib
import numpy as np
import os
from config.paths_config import MODEL_OUTPUT_PATH
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# path to the frontend build directory (Vite/React)
FRONTEND_DIST = os.path.join(os.getcwd(), "hotel-predict-sparkle-main", "dist")

# load model safely at startup; if it fails keep loaded_model = None
loaded_model = None
if os.path.exists(MODEL_OUTPUT_PATH):
    try:
        loaded_model = joblib.load(MODEL_OUTPUT_PATH)
    except Exception:
        # don't raise here; keep running so the app doesn't crash on missing/invalid model
        loaded_model = None


@app.route('/api/predict', methods=['POST'])
def api_predict():
    if loaded_model is None:
        return jsonify({"error": "Model not loaded"}), 500

    payload = request.get_json()
    if not payload:
        return jsonify({"error": "JSON body required"}), 400

    try:
        features = [
            int(payload["lead_time"]),
            int(payload["no_of_special_request"]),
            float(payload["avg_price_per_room"]),
            int(payload["arrival_month"]),
            int(payload["arrival_date"]),
            int(payload["market_segment_type"]),
            int(payload["no_of_week_nights"]),
            int(payload["no_of_weekend_nights"]),
            int(payload["type_of_meal_plan"]),
            int(payload["room_type_reserved"]),
        ]
    except KeyError as ke:
        return jsonify({"error": f"Missing field: {ke}"}), 400
    except ValueError:
        return jsonify({"error": "Invalid field types"}), 400

    arr = np.array(features).reshape(1, -1)
    pred = int(loaded_model.predict(arr)[0])
    return jsonify({"prediction": pred})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    """
    If the frontend build directory exists, serve the SPA static files (index.html + assets).
    Otherwise fall back to the server-rendered `templates/index.html` form behavior.
    """
    # Serve built frontend when available
    if os.path.exists(FRONTEND_DIST):
        # if a static asset is requested and exists, serve it; otherwise return index.html
        if path != "" and os.path.exists(os.path.join(FRONTEND_DIST, path)):
            return send_from_directory(FRONTEND_DIST, path)
        return send_from_directory(FRONTEND_DIST, 'index.html')

    # fallback: server-rendered form (existing behavior)
    if request.method == 'POST':
        try:
            lead_time = int(request.form.get("lead_time"))
            no_of_special_request = int(request.form.get("no_of_special_request"))
            avg_price_per_room = float(request.form.get("avg_price_per_room"))
            arrival_month = int(request.form.get("arrival_month"))
            arrival_date = int(request.form.get("arrival_date"))

            market_segment_type = int(request.form.get("market_segment_type"))
            no_of_week_nights = int(request.form.get("no_of_week_nights"))
            no_of_weekend_nights = int(request.form.get("no_of_weekend_nights"))

            type_of_meal_plan = int(request.form.get("type_of_meal_plan"))
            room_type_reserved = int(request.form.get("room_type_reserved"))

            features = np.array([[lead_time, no_of_special_request, avg_price_per_room, arrival_month, arrival_date, market_segment_type, no_of_week_nights, no_of_weekend_nights, type_of_meal_plan, room_type_reserved]])

            if loaded_model is None:
                return render_template('index.html', prediction=None, error='Model not available')

            prediction = loaded_model.predict(features)
            return render_template('index.html', prediction=prediction[0])
        except (TypeError, ValueError):
            return render_template('index.html', prediction=None, error='Invalid input')

    return render_template("index.html", prediction=None)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
