from fastapi import FastAPI, HTTPException
import httpx
import os

app = FastAPI(title="SnapWeather API")

@app.get("/")
def home():
    # Reads the environment variable from SnapDeploy; defaults to New York if empty
    default_city = os.getenv("DEFAULT_CITY", "New York")
    return {
        "status": "online",
        "configured_default_city": default_city,
        "message": f"Welcome to SnapWeather! Try looking up your default city, or append /weather/cityname to the URL."
    }

@app.get("/weather/{city}")
async def get_weather(city: str):
    try:
        async with httpx.AsyncClient() as client:
            # Step 1: Find coordinates for the city using Open-Meteo
            geo_url = f"https://open-meteo.com{city}&count=1&language=en&format=json"
            geo_res = await client.get(geo_url)
            geo_data = geo_res.json()
            
            if not geo_data.get("results"):
                raise HTTPException(status_code=404, detail=f"City '{city}' not found")
                
            location = geo_data["results"][0]
            lat, lon = location["latitude"], location["longitude"]
            
            # Step 2: Get current live weather temperature
            weather_url = f"https://open-meteo.com{lat}&longitude={lon}&current_weather=true"
            weather_res = await client.get(weather_url)
            weather_data = weather_res.json()
            
            return {
                "city": location["name"],
                "country": location.get("country", "Unknown"),
                "temperature_celsius": weather_data["current_weather"]["temperature"],
                "windspeed_kmh": weather_data["current_weather"]["windspeed"],
                "latitude": lat,
                "longitude": lon
            }
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

