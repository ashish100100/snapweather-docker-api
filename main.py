from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import httpx

app = FastAPI()

# HTML template with an input form and mobile-friendly styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Docker Weather App</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; background-color: #eef2f3; margin: 0; padding: 20px; box-sizing: border-box; }
        .card { background: white; padding: 25px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; }
        h2 { color: #0284c7; margin-bottom: 20px; font-size: 22px; }
        input { width: 100%; padding: 12px; margin-bottom: 15px; border: 2px solid #cbd5e1; border-radius: 8px; font-size: 16px; box-sizing: border-box; outline: none; }
        input:focus { border-color: #0284c7; }
        button { width: 100%; background-color: #0284c7; color: white; border: none; padding: 12px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold; }
        button:hover { background-color: #0369a1; }
        .result { margin-top: 25px; padding: 15px; background: #f8fafc; border-radius: 8px; border-left: 4px solid #0284c7; text-align: left; }
        .error { color: #dc2626; margin-top: 15px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🌤️ Docker Weather App</h2>
        <form method="GET" action="/">
            <input type="text" name="city" placeholder="Enter city name (e.g. Paris)" required autocomplete="off">
            <button type="submit">Get Weather</button>
        </form>
        {content}
    </div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def get_weather_page(city: str = None):
    if not city:
        # Default home screen before typing anything
        return HTML_TEMPLATE.format(content="")

    url = f"https://wttr.in{city}?format=j1"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code != 200:
                raise HTTPException(status_code=404)
            
            data = response.json()
            current = data["current_condition"][0]
            temp = current["temp_C"]
            desc = current["weatherDesc"][0]["value"]
            humidity = current["humidity"]
            wind = current["windspeedKmph"]

            # Format the output inside our UI card
            result_html = f"""
            <div class="result">
                <h3>📍 {city.capitalize()}</h3>
                <p><strong>Temperature:</strong> {temp}°C</p>
                <p><strong>Condition:</strong> {desc}</p>
                <p><strong>Humidity:</strong> {humidity}%</p>
                <p><strong>Wind Speed:</strong> {wind} km/h</p>
            </div>
            """
            return HTML_TEMPLATE.format(content=result_html)
            
        except Exception:
            error_html = f'<p class="error">❌ Could not find weather for "{city}". Try checking the spelling.</p>'
            return HTML_TEMPLATE.format(content=error_html)
            

