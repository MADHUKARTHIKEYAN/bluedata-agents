from typing import Any, Dict
import httpx


def get_marine_conditions(
    latitude: float = 13.110721,
    longitude: float = 80.2459,
    location_name: str = "Chennai Coastal Zone",
) -> Dict[str, Any]:
    """
    Fetch live marine conditions from Open-Meteo Marine API.
    """

    url = "https://marine-api.open-meteo.com/v1/marine"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "wave_height",
            "wave_direction",
            "wave_period",
            "wind_wave_height",
            "wind_wave_direction",
            "wind_wave_period",
            "swell_wave_height",
            "swell_wave_direction",
            "swell_wave_period",
        ],
        "hourly": [
            "wave_height",
            "wave_period",
            "wind_wave_height",
            "swell_wave_height",
        ],
        "timezone": "auto",
    }

    try:
        with httpx.Client(timeout=15.0) as client:
            response = client.get(url, params=params)
            response.raise_for_status()

            data = response.json()

        current = data.get("current", {})

        wave_height = current.get("wave_height")
        wave_period = current.get("wave_period")

        return {
            "status": "success",
            "location": location_name,
            "latitude": latitude,
            "longitude": longitude,
            "current": {
                "wave_height": wave_height,
                "wave_direction": current.get("wave_direction"),
                "wave_period": wave_period,
                "wind_wave_height": current.get("wind_wave_height"),
                "wind_wave_direction": current.get("wind_wave_direction"),
                "wind_wave_period": current.get("wind_wave_period"),
                "swell_wave_height": current.get("swell_wave_height"),
                "swell_wave_direction": current.get("swell_wave_direction"),
                "swell_wave_period": current.get("swell_wave_period"),
            },
        }

    except Exception as err:
        return {
            "status": "error",
            "location": location_name,
            "latitude": latitude,
            "longitude": longitude,
            "error": str(err),
        }


if __name__ == "__main__":
    print("🌊 Testing REAL Marine API...")

    result = get_marine_conditions()

    print("\n==============================")
    print("LIVE MARINE DATA")
    print("==============================")
    print(result)   
