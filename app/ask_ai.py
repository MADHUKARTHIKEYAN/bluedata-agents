import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_ai(prompt: str) -> str:
    """
    Send a prompt to Groq and return the generated response.
    """

    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY is not set in the .env file")

    print("🟢 Trying Groq...")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.2,
    )

    result = response.choices[0].message.content

    print("✅ Groq response received")

    return result