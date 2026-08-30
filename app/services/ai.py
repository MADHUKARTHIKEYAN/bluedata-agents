from .groq import ask_groq
from .gemini import ask_gemini
from .sarvam import ask_sarvam


def ask_ai(prompt: str) -> str:
    """
    Multi-provider AI fallback.

    Order:
    1. Groq
    2. Gemini
    3. Sarvam
    """

    # -------------------------------------------------
    # 1. GROQ
    # -------------------------------------------------
    print("🟢 Trying Groq...")

    try:
        result = ask_groq(prompt)

        if result:
            print("✅ Groq response received")
            return result

    except Exception as error:
        print(f"⚠️ Groq failed: {error}")

    # -------------------------------------------------
    # 2. GEMINI
    # -------------------------------------------------
    print("🧠 Trying Gemini...")

    try:
        result = ask_gemini(prompt)

        if result:
            print("✅ Gemini response received")
            return result

    except Exception as error:
        print(f"⚠️ Gemini failed: {error}")

    # -------------------------------------------------
    # 3. SARVAM
    # -------------------------------------------------
    print("🇮🇳 Trying Sarvam...")

    try:
        result = ask_sarvam(prompt)

        if result:
            print("✅ Sarvam response received")
            return result

    except Exception as error:
        print(f"⚠️ Sarvam failed: {error}")

    # -------------------------------------------------
    # ALL PROVIDERS FAILED
    # -------------------------------------------------
    return (
        "AI services are temporarily unavailable. "
        "Please try again shortly."
    )