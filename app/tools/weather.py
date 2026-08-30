from typing import Any, Dict, Optional
import httpx


def get_weather_forecast(
    latitude: float = 13.110721,
    longitude: float = 80.2459,
    location_name: Optional[str] = "Chennai Coastal Zone",
) -> Dict[str, Any]:

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,

        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m",
            "wind_direction_10m",
            "wind_gusts_10m",
        ],

        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "precipitation_probability_max",
            "wind_speed_10m_max",
            "wind_gusts_10m_max",
        ],

        "hourly": [
            "wind_speed_10m",
            "wind_gusts_10m",
            "precipitation_probability",
            "precipitation",
        ],

        "forecast_days": 2,
        "timezone": "auto",
    }

    try:

        with httpx.Client(timeout=10.0) as client:

            response = client.get(url, params=params)

            response.raise_for_status()

            data = response.json()

            current = data.get("current", {})
            daily = data.get("daily", {})

            return {
                "status": "success",

                "location": location_name,

                "latitude": latitude,
                "longitude": longitude,

                "current": {
                    "temperature": current.get("temperature_2m"),
                    "wind_speed": current.get("wind_speed_10m"),
                    "wind_gusts": current.get("wind_gusts_10m"),
                    "wind_direction": current.get("wind_direction_10m"),
                    "precipitation": current.get("precipitation"),
                    "humidity": current.get(
                        "relative_humidity_2m"
                    ),
                },

                "forecast": {
                    "dates": daily.get("time"),

                    "temperature_max": daily.get(
                        "temperature_2m_max"
                    ),

                    "temperature_min": daily.get(
                        "temperature_2m_min"
                    ),

                    "precipitation": daily.get(
                        "precipitation_sum"
                    ),

                    "precipitation_probability": daily.get(
                        "precipitation_probability_max"
                    ),

                    "wind_speed_max": daily.get(
                        "wind_speed_10m_max"
                    ),

                    "wind_gusts_max": daily.get(
                        "wind_gusts_10m_max"
                    ),
                },
            }

    except Exception as err:

        return {
            "status": "error",
            "location": location_name,
            "error": str(err),
        }