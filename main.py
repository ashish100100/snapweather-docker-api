from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(title="SnapWeather API")

@app.get("/")
def home():
    return {"status": "online", "message": "Welcome to SnapWeather! Append /weather/cityname to the URL."}

@app.get("/weather/{city}")
async def get_weather(city: str):
    # Uses the open-source, no-auth Open-Meteo geocoding and weather APIs
    try:
        async with httpx.AsyncClient() as client:
            # Step 1: Find coordinates for the city
            geo_url = f"https://open-meteo.com{city}&count=1&language=en&format=json"
            geo_res = await client.get(geo_url)
            geo_data = geo_res.json()
            
            if not geo_data.get("results"):
                raise HTTPException(status_code=404, detail="City not found")
                
            location = geo_data["results"][0]
            lat, lon = location["latitude"], location["longitude"]
            
            # Step 2: Get current temperature
            weather_url = f"https://open-meteo.com{lat}&longitude={lon}&current_weather=true"
            weather_res = await client.get(weather_url)
            weather_data = weather_res.json()
            
            return {
                "city": location["name"],
                "country": location.get("country", "Unknown"),
                "temperature_celsius": weather_data["current_weather"]["temperature"],
                "windspeed": weather_data["current_weather"]["windspeed"]
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
          
