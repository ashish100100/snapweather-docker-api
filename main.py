
from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Weather API is running ☁️ Use /weather?city=Ludhiana"

@app.route("/weather")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))  # Snapdeploy sets PORT automatically
    app.run(host="0.0.0.0", port=port)
    
def weather():
    city = request.args.get("city", "Ludhiana")
    url = f"https://wttr.in/{city}?format=j1"

    try:
        res = requests.get(url, timeout=10)
        data = res.json()

        current = data["current_condition"][0]
        result = {
            "city": city,
            "temperature_c": current["temp_C"],
            "feels_like_c": current["FeelsLikeC"],
            "weather": current["weatherDesc"][0]["value"],
            "humidity": current["humidity"],
            "wind_kmph": current["windspeedKmph"]
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
