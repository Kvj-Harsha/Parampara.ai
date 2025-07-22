import requests

# === CONFIG ===
GEMINI_API_KEY = "AIzaSyCmbqRVGrz0580prVn1_hH5Y_kQR5qksfc"  # Replace this with your actual API key
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


# === Function to translate Telugu text ===
def translate_telugu_to_english(telugu_text):
    prompt = f"""
Translate the following Telugu passage into clear, natural English.
Preserve meaning and tone.

Telugu:
\"\"\"{telugu_text.strip()}\"\"\"
"""

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=payload,
            timeout=15
        )
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    except KeyError:
        return "Error: Unexpected response format from Gemini API"

# === Sample Telugu input ===
if __name__ == "__main__":
    telugu_input = input("Enter Telugu text: ")
    translation = translate_telugu_to_english(telugu_input)
    print("\n🌍 Translated English:\n")
    print(translation)
