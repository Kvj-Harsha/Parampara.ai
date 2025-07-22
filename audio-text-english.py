import streamlit as st
import whisper
import tempfile
import time
import os
import requests
import json
import uuid
from datetime import datetime
import pathlib
from dotenv import load_dotenv
load_dotenv()

# --- CONFIG ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # 🔐 Replace with your actual Gemini API Key
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# Load Whisper model
model = whisper.load_model("tiny")

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Whisper Telugu STT + Gemini Translation", layout="centered")
st.title("🗣️ Whisper STT + Gemini – Telugu Audio to English Translation")
st.markdown("""
Upload a short audio clip (10–30 seconds) in **Telugu**.

🔊 **Whisper** will transcribe it offline.  
🧠 **Gemini (Google AI)** will translate it to **English**.

> ✅ No Whisper API needed – only Gemini for translation!
""")

# --- Session State Initialization ---
if "telugu_text" not in st.session_state:
    st.session_state.telugu_text = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

# --- User Metadata ---
st.subheader("🧾 Additional Info")
username = st.text_input("👤 Your Name")
latitude = st.text_input("📍 Latitude", placeholder="Optional")
longitude = st.text_input("📍 Longitude", placeholder="Optional")
category = st.selectbox("📁 Category", ["Story", "Interview", "News", "Other"])

# --- File Upload ---
audio_file = st.file_uploader("📤 Upload an audio file", type=["mp3", "wav", "m4a", "mp4"])

if audio_file is not None:
    ext = pathlib.Path(audio_file.name).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_audio:
        temp_audio.write(audio_file.read())
        temp_path = temp_audio.name

    st.audio(temp_path)

    # Transcribe Button
    if st.button("📝 Transcribe Audio in Telugu"):
        try:
            start_time = time.time()
            with st.spinner("Transcribing..."):
                result = model.transcribe(temp_path, language="te", task="transcribe")
            st.session_state.telugu_text = result["text"]
            duration = time.time() - start_time
            st.success(f"✅ Transcription completed in {duration:.2f} seconds")
        except Exception as e:
            st.error(f"Transcription failed: {e}")
        finally:
            os.remove(temp_path)

# Display transcription (if available)
if st.session_state.telugu_text:
    st.text_area("📝 Telugu Transcript", st.session_state.telugu_text, height=250)

    # Save Function
    def save_data(transcription, translation, prompt, username, latitude, longitude, category):
        os.makedirs("data", exist_ok=True)
        file_id = str(uuid.uuid4())
        data = {
            "id": file_id,
            "timestamp": datetime.now().isoformat(),
            "username": username,
            "coordinates": {
                "latitude": latitude,
                "longitude": longitude
            },
            "category": category,
            "transcription_telugu": transcription,
            "translation_english": translation,
            "system_prompt": prompt
        }
        with open(f"data/{file_id}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return file_id

    if st.button("🌐 Translate to English using Gemini"):
        prompt = f"""You are a professional translator. Translate the following Telugu text into fluent, natural English. Ensure the meaning, tone, and context are preserved. The input corpus might contain a mix of other languages and grammatical errors. Focus on the essence of the content. Do not display any header or footer, only the translated story.

Telugu:
\"\"\"{st.session_state.telugu_text.strip()}\"\"\""""

        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        try:
            with st.spinner("Translating using Gemini..."):
                response = requests.post(
                    f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
                    headers=headers,
                    json=payload,
                    timeout=15
                )
                response.raise_for_status()
                translation = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                st.session_state.translated_text = translation
                st.success("✅ Translation completed")

                # Save to JSON
                file_id = save_data(
                    transcription=st.session_state.telugu_text,
                    translation=translation,
                    prompt=prompt,
                    username=username,
                    latitude=latitude,
                    longitude=longitude,
                    category=category
                )
                st.info(f"📁 Data saved as `data/{file_id}.json`")

        except Exception as e:
            st.error(f"Translation failed: {e}")

# Display translation (if available)
if st.session_state.translated_text:
    st.text_area("🌍 English Translation", st.session_state.translated_text, height=300)
