from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END

from app.tools.marine import get_marine_conditions
from app.tools.weather import get_weather_forecast
from app.services.ai import ask_ai
from app.tools.safety import calculate_safety_risk

from .state import AgentState


# Load environment variables
load_dotenv()


# --------------------------------
# 1. PLANNER AGENT
# --------------------------------

def planner_agent(state: AgentState):

    user_input = state["user_input"]

    print(f"🧠 Planner received: {user_input}")

    prompt = f"""
You are the Planner Agent for a smart marine and fishing assistance system.

Classify the user's request into exactly ONE of these categories:

- ocean
- weather
- safety

Definitions:

ocean:
Questions about fishing zones, ocean conditions, sea surface temperature,
chlorophyll, potential fishing zones, currents, waves, or marine resources.

weather:
Questions about rain, wind, storms, cyclones, weather forecasts,
temperature, or upcoming weather conditions.

safety:
Questions about whether it is safe to go fishing, marine danger,
warnings, vessel safety, risk levels, or dangerous sea conditions.

User request:
{user_input}

Return ONLY one word:
ocean
weather
safety
"""

    result = ask_ai(prompt)

    intent = result.strip().lower()

    # Safety fallback if model returns extra text
    if "weather" in intent:
        intent = "weather"
    elif "safety" in intent:
        intent = "safety"
    else:
        intent = "ocean"

    print(f"📋 Planner intent: {intent}")

    return {
        "intent": intent
    }


# --------------------------------
# 2. OCEAN AGENT
# --------------------------------

def ocean_agent(state: AgentState):

    print("🌊 Ocean Agent activated")

    # Fetch live marine conditions
    marine_data = get_marine_conditions()

    print("🌐 Live marine data received:")
    print(marine_data)

    if marine_data["status"] != "success":
        return {
            "response": (
                "Unable to retrieve live marine conditions right now."
            )
        }

    current = marine_data["current"]

    prompt = f"""
You are a marine intelligence assistant helping fishermen.

Analyze the following LIVE marine conditions:

Location: {marine_data['location']}
Latitude: {marine_data['latitude']}
Longitude: {marine_data['longitude']}

Wave height: {current['wave_height']} m
Wave direction: {current['wave_direction']}°
Wave period: {current['wave_period']} seconds

Wind-wave height: {current['wind_wave_height']} m
Wind-wave direction: {current['wind_wave_direction']}°
Wind-wave period: {current['wind_wave_period']} seconds

Swell height: {current['swell_wave_height']} m
Swell direction: {current['swell_wave_direction']}°
Swell period: {current['swell_wave_period']} seconds

The user asked:
{state["user_input"]}

Explain what these conditions mean for a fisherman.

Give:

1. Sea condition
2. Expected boat stability
3. Fishing suitability
4. Main concern
5. Simple recommendation

Do not invent weather or ocean measurements that are not provided.

Keep the explanation practical and easy for a fisherman to understand.
"""

    analysis = ask_ai(prompt)

    print("🧠 AI ocean analysis:")
    print(analysis)

    return {
        "response": analysis
    }


# --------------------------------
# 3. WEATHER AGENT
# --------------------------------

def weather_agent(state: AgentState):

    print("🌦️ Weather Agent activated")

    # ==================================================
    # 1. GET LIVE WEATHER DATA
    # ==================================================

    weather = get_weather_forecast()

    print("🌐 Live weather data received:")
    print(weather)

    # Check weather API status
    if weather.get("status") != "success":
        return {
            "response": (
                "Unable to retrieve live weather conditions right now. "
                "Please try again shortly."
            )
        }

    # ==================================================
    # 2. EXTRACT FORECAST DATA
    # ==================================================

    forecast = weather.get("forecast", {})

    dates = forecast.get("dates", [])
    temperature_max = forecast.get("temperature_max", [])
    temperature_min = forecast.get("temperature_min", [])
    precipitation = forecast.get("precipitation", [])
    precipitation_probability = forecast.get(
        "precipitation_probability", []
    )
    wind_speed_max = forecast.get("wind_speed_max", [])
    wind_gusts_max = forecast.get("wind_gusts_max", [])

    # ==================================================
    # 3. CHECK TOMORROW'S DATA
    # ==================================================

    if len(dates) < 2:
        return {
            "response": (
                "Tomorrow's weather forecast is currently unavailable."
            )
        }

    required_data = [
        temperature_max,
        temperature_min,
        precipitation,
        precipitation_probability,
        wind_speed_max,
        wind_gusts_max,
    ]

    if any(len(data) < 2 for data in required_data):
        return {
            "response": (
                "Tomorrow's complete weather forecast is currently "
                "unavailable."
            )
        }

    # ==================================================
    # 4. EXTRACT TOMORROW'S FORECAST
    # ==================================================

    tomorrow_data = {
        "date": dates[1],
        "temperature_max": temperature_max[1],
        "temperature_min": temperature_min[1],
        "precipitation": precipitation[1],
        "precipitation_probability": precipitation_probability[1],
        "wind_speed_max": wind_speed_max[1],
        "wind_gusts_max": wind_gusts_max[1],
    }

    print("📅 Tomorrow's forecast:")
    print(tomorrow_data)

    # ==================================================
    # 5. CREATE AI PROMPT
    # ==================================================

    prompt = f"""
You are a marine weather assistant helping fishermen.

The user asked:
"{state["user_input"]}"

Location:
{weather.get("location", "Unknown")}

The user is asking about TOMORROW.

Today's date:
{dates[0]}

Tomorrow's date:
{tomorrow_data["date"]}

Use ONLY the following TOMORROW forecast data:

Temperature maximum:
{tomorrow_data["temperature_max"]} °C

Temperature minimum:
{tomorrow_data["temperature_min"]} °C

Maximum wind speed:
{tomorrow_data["wind_speed_max"]} km/h

Maximum wind gusts:
{tomorrow_data["wind_gusts_max"]} km/h

Rain:
{tomorrow_data["precipitation"]} mm

Rain probability:
{tomorrow_data["precipitation_probability"]}%

Answer the user's question specifically for a fisherman.

Explain:

1. Temperature
2. Wind conditions
3. Wind gust risk
4. Rain probability
5. Practical fishing recommendation

IMPORTANT RULES:

- Use TOMORROW'S values only.
- Do not use today's weather values.
- Do not invent weather measurements.
- Do not invent wave conditions.
- Do not claim the sea is safe unless the provided data supports that conclusion.
- Do not infer what time of day wind, rain, or gusts will occur.
- Do not say conditions will be better in the morning or worse in the afternoon unless hourly data is provided.
- Do not say rain or wind is likely at a specific time unless hourly data is provided.
- Clearly distinguish between forecast maximums and actual conditions.
- Keep the explanation simple and understandable for fishermen.
- Give a short practical recommendation.
"""

    # ==================================================
    # 6. AI ANALYSIS
    # ==================================================

    # IMPORTANT:
    # Use ask_ai() so the system automatically tries:
    #
    # Groq → Gemini → Sarvam
    #
    # if one provider fails.

    ai_response = ask_ai(prompt)

    print("🧠 AI weather analysis:")
    print(ai_response)

    # ==================================================
    # 7. RETURN RESULT
    # ==================================================

    return {
        "response": ai_response
    }
# --------------------------------
# 4. SAFETY AGENT
# --------------------------------

def safety_agent(state: AgentState):

    print("🚨 Safety Agent activated")

    user_input = state["user_input"]

    # --------------------------------
    # GET LIVE MARINE DATA
    # --------------------------------

    marine_data = get_marine_conditions()

    print("🌊 Live marine data for safety:")
    print(marine_data)

    if marine_data.get("status") != "success":

        return {
            "response": (
                "⚠️ Live marine conditions are unavailable. "
                "Please check official marine warnings before going to sea."
            )
        }

    # --------------------------------
    # GET LIVE WEATHER DATA
    # --------------------------------

    weather_data = get_weather_forecast()

    print("🌦️ Live weather data for safety:")
    print(weather_data)

    if weather_data.get("status") != "success":

        return {
            "response": (
                "⚠️ Live weather conditions are unavailable. "
                "Please check official weather warnings before going to sea."
            )
        }

    # --------------------------------
    # EXTRACT MARINE VALUES
    # --------------------------------

    marine_current = marine_data.get("current", {})

    wave_height = marine_current.get(
        "wave_height",
        "N/A"
    )

    swell_height = marine_current.get(
        "swell_wave_height",
        "N/A"
    )

    wave_period = marine_current.get(
        "wave_period",
        "N/A"
    )

    wave_direction = marine_current.get(
        "wave_direction",
        "N/A"
    )

    swell_period = marine_current.get(
        "swell_wave_period",
        "N/A"
    )

    # --------------------------------
    # EXTRACT WEATHER VALUES
    # --------------------------------

    weather_current = weather_data.get("current", {})

    wind_speed = weather_current.get(
        "wind_speed",
        "N/A"
    )

    wind_gusts = weather_current.get(
        "wind_gusts",
        "N/A"
    )

    wind_direction = weather_current.get(
        "wind_direction",
        "N/A"
    )

    temperature = weather_current.get(
        "temperature",
        "N/A"
    )

    precipitation = weather_current.get(
        "precipitation",
        "N/A"
    )

    humidity = weather_current.get(
        "humidity",
        "N/A"
    )

    # --------------------------------
    # DETERMINISTIC SAFETY ENGINE
    # --------------------------------

    safety_result = calculate_safety_risk(
        wave_height=wave_height,
        wind_speed=wind_speed,
        wind_gusts=wind_gusts,
        swell_height=swell_height,
    )

    risk_level = safety_result["risk_level"]
    risk_score = safety_result["risk_score"]
    risk_reasons = safety_result["reasons"]

    print("📊 Safety rule engine result:")
    print(safety_result)

    # --------------------------------
    # CONVERT RISK TO USER-FRIENDLY LABEL
    # --------------------------------

    if risk_level == "LOW":

        risk_label = "🟢 LOW RISK"

    elif risk_level == "MODERATE":

        risk_label = "🟡 MODERATE RISK"

    else:

        risk_label = "🔴 HIGH RISK"

    # --------------------------------
    # AI EXPLANATION
    # --------------------------------

    prompt = f"""
You are a marine safety assistant helping fishermen.

The user asked:

"{user_input}"

The deterministic safety engine has already calculated the
risk level.

IMPORTANT:
You MUST use the provided risk level.
Do NOT change it.
Do NOT invent another risk level.

DETERMINISTIC SAFETY RESULT:

Risk level:
{risk_level}

Risk score:
{risk_score}

Risk factors:
{risk_reasons}


LIVE MARINE CONDITIONS:

Location:
{marine_data.get("location", "Unknown")}

Wave height:
{wave_height} m

Wave period:
{wave_period} seconds

Wave direction:
{wave_direction} degrees

Swell height:
{swell_height} m

Swell period:
{swell_period} seconds


LIVE WEATHER CONDITIONS:

Temperature:
{temperature} °C

Wind speed:
{wind_speed} km/h

Wind gusts:
{wind_gusts} km/h

Wind direction:
{wind_direction} degrees

Precipitation:
{precipitation} mm

Humidity:
{humidity}%


Write a clear explanation for a fisherman.

Use this structure:

### Safety Assessment

{risk_label}

### Marine Conditions

Explain the current wave and swell conditions.

### Wind Conditions

Explain the current wind and gust conditions.

### Fishing Risk

Explain how these conditions may affect fishing.

### Main Dangers

List the most important risks.

### Recommendation

Give a practical safety recommendation.

IMPORTANT:

- Do not change the calculated risk level.
- Do not invent measurements.
- Do not claim that going to sea is completely safe.
- Clearly mention uncertainty.
- This is an AI assessment, not an official marine warning.

End with:

"Always check official marine and weather warnings before going to sea."
"""

    # --------------------------------
    # MULTI-PROVIDER AI
    # --------------------------------

    analysis = ask_ai(prompt)

    print("🧠 AI safety analysis:")
    print(analysis)

    return {
        "response": analysis
    }

# --------------------------------
# ROUTER
# --------------------------------

def route_to_agent(state: AgentState):

    intent = state["intent"]

    if intent == "weather":
        return "weather"

    if intent == "safety":
        return "safety"

    return "ocean"


# --------------------------------
# BUILD GRAPH
# --------------------------------

def build_graph():

    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_agent)
    graph.add_node("ocean", ocean_agent)
    graph.add_node("weather", weather_agent)
    graph.add_node("safety", safety_agent)

    graph.add_edge(START, "planner")

    graph.add_conditional_edges(
        "planner",
        route_to_agent,
        {
            "ocean": "ocean",
            "weather": "weather",
            "safety": "safety",
        },
    )

    graph.add_edge("ocean", END)
    graph.add_edge("weather", END)
    graph.add_edge("safety", END)

    return graph.compile()


app_graph = build_graph()