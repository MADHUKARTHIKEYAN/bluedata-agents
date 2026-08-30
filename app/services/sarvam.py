import os
from dotenv import load_dotenv
from sarvamai import SarvamAI

load_dotenv()

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

if not SARVAM_API_KEY:
    raise ValueError("SARVAM_API_KEY is missing from .env")

client = SarvamAI(
    api_subscription_key=SARVAM_API_KEY
)


def ask_sarvam(prompt: str) -> str:
    response = client.chat.completions(
        model="sarvam-105b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.2,
        max_tokens=1000,
        reasoning_effort=None,
    )

    return response.choices[0].message.content