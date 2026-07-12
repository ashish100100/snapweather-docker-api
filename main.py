

import os
import secrets
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Load SECRET_KEY from Snapdeploy env. If not set, generate a random one
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", secrets.token_hex(32))

@app.route("/")
def home():
    return "Weather API is running ☁️ Use /weather?city=Ludhiana"

@app.route("/weather")
def weather():
    city = request.args.get("city", "Majitha")
    url = f"https://wttr.in/{city}?format=j1"

    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()

        current = data["current_condition"][0]
        result = {
            "city": city,
            "temperature_c": current["temp_C"],
            "feels_like_c": current["FeelsLikeC"],
            "weather": current["weatherDesc"][0]["value"],
            "humidity": current["humidity"] + "%",
            "wind_kmph": current["windspeedKmph"] + " km/h"
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": "Could not fetch weather", "details": str(e)}), 500

@app.route("/health")
def health():
    return jsonify({"status": "ok", "app": "docker-weather"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000)) # Snapdeploy sets PORT
    app.run(host="0.0.0.0", port=port)
