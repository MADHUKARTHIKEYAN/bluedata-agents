"""Tools package for marine, weather, and safety analytics."""

from .marine import get_marine_conditions
from .weather import get_weather_forecast

__all__ = [
    "get_marine_conditions",
    "get_weather_forecast",
]