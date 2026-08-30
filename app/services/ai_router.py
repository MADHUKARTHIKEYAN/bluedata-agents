from .gemini import ask_gemini
from .groq import ask_groq
from .sarvam import ask_sarvam


def ask_ai(prompt: str) -> str:

    # -------------------------
    # 1. Gemini
    # -------------------------

    try:
        print("🤖 AI Router → Gemini")

        result = ask_gemini(prompt)

        if result:
            return result

    except Exception as e:
        print(f"⚠️ Gemini failed: {e}")


    # -------------------------
    # 2. Groq
    # -------------------------

    try:
        print("⚡ AI Router → Groq")

        result = ask_groq(prompt)

        if result:
            return result

    except Exception as e:
        print(f"⚠️ Groq failed: {e}")


    # -------------------------
    # 3. Sarvam
    # -------------------------

    try:
        print("🇮🇳 AI Router → Sarvam")

        result = ask_sarvam(prompt)

        if result:
            return result

    except Exception as e:
        print(f"⚠️ Sarvam failed: {e}")


    # -------------------------
    # 4. Final fallback
    # -------------------------

    return (
        "AI analysis is temporarily unavailable. "
        "Please rely on the latest sensor and weather data."
    )