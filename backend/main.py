from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os

API_KEY = os.getenv("API_KEY")

cities = [
    {"name": "Lagos", "lat": 6.5244, "lon": 3.3792},
    {"name": "Port Harcourt", "lat": 4.8156, "lon": 7.0498},
    {"name": "Abuja", "lat": 9.0765, "lon": 7.3986},
    {"name": "Kano", "lat": 12.0022, "lon": 8.5920}
]

@app.get("/risk")
def get_risk():

    results = []

    # 🌧️ FLOOD DATA
    for city in cities:

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city['name']}&appid={API_KEY}"
        response = requests.get(url).json()

        rain = response.get("rain", {}).get("1h", 0)

        if rain > 15:
            risk = "High"
            trend = "Critical"
            recommendation = "Immediate evacuation recommended"

        elif rain > 8:
            risk = "High"
            trend = "Rising"
            recommendation = "Emergency teams should prepare"

        elif rain > 3:
            risk = "Medium"
            trend = "Increasing"
            recommendation = "Monitor flood-prone areas"

        else:
            risk = "Low"
            trend = "Stable"
            recommendation = "Situation stable"

        results.append({
            "zone": city["name"],
            "lat": city["lat"],
            "lon": city["lon"],
            "risk_level": risk,
            "trend": trend,
            "recommendation": recommendation,
            "type": "Flood"
        })

    # 🌎 EARTHQUAKE DATA
    eq_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
    eq_data = requests.get(eq_url).json()

    for eq in eq_data["features"][:5]:

        coords = eq["geometry"]["coordinates"]
        mag = eq["properties"]["mag"]

        results.append({
            "zone": "Earthquake Event",
            "lat": coords[1],
            "lon": coords[0],
            "risk_level": "High" if mag >= 5 else "Medium",
            "trend": "Active",
            "recommendation": f"Magnitude {mag} earthquake detected",
            "type": "Earthquake"
        })

    return {"data": results}