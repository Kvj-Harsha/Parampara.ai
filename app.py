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

# Load environment variables (ensure .env file exists with GEMINI_API_KEY)
load_dotenv()

# --- CONFIG ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# Ensure GEMINI_API_KEY is set
if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY not found. Please set it in your .env file.")
    st.stop()

# Load Whisper model (cache it to avoid reloading on every rerun)
@st.cache_resource
def load_whisper_model():
    """Loads the Whisper 'tiny' model."""
    return whisper.load_model("tiny")

model = load_whisper_model()

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

# --- User Metadata Section (using st.expander for a cleaner look) ---
with st.expander("🧾 Additional Information (Optional)", expanded=False):
    st.markdown("Provide optional details about the audio.")
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("👤 Your Name", key="username_input")
    with col2:
        category = st.selectbox("📁 Category", ["Story", "Interview", "News", "Other"], key="category_select")

    col3, col4 = st.columns(2)
    with col3:
        latitude = st.text_input("📍 Latitude", placeholder="e.g., 17.3850", key="latitude_input")
    with col4:
        longitude = st.text_input("📍 Longitude", placeholder="e.g., 78.4867", key="longitude_input")

# --- File Upload Section ---
st.subheader("Upload Audio")
audio_file = st.file_uploader("📤 Upload an audio file", type=["mp3", "wav", "m4a", "mp4"])

temp_path = None # Initialize temp_path outside the if block

if audio_file is not None:
    ext = pathlib.Path(audio_file.name).suffix
    # Create a temporary file to save the uploaded audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_audio:
        temp_audio.write(audio_file.read())
        temp_path = temp_audio.name

    st.audio(temp_path, format=f"audio/{ext.lstrip('.')}") # Display the audio player

    # --- Transcription Button ---
    if st.button("📝 Transcribe Audio in Telugu", use_container_width=True):
        if temp_path: # Ensure temp_path exists before transcribing
            try:
                start_time = time.time()
                with st.spinner("Transcribing audio with Whisper... This might take a moment."):
                    # Transcribe the audio using the loaded Whisper model
                    result = model.transcribe(temp_path, language="te", task="transcribe")
                st.session_state.telugu_text = result["text"]
                duration = time.time() - start_time
                st.success(f"✅ Transcription completed in {duration:.2f} seconds!")
            except Exception as e:
                st.error(f"Transcription failed: {e}")
            finally:
                # Clean up the temporary file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        else:
            st.warning("Please upload an audio file first.")

# --- Display Transcription and Translation Sections ---
if st.session_state.telugu_text:
    st.subheader("Transcription & Translation")
    st.text_area("📝 Telugu Transcript", st.session_state.telugu_text, height=180, disabled=True)

    # --- Save Data Function ---
    def save_data(transcription, translation, prompt_text, username_val, latitude_val, longitude_val, category_val):
        """Saves transcription and translation data to a JSON file."""
        os.makedirs("data", exist_ok=True) # Ensure 'data' directory exists
        file_id = str(uuid.uuid4()) # Generate a unique ID for the file
        data = {
            "id": file_id,
            "timestamp": datetime.now().isoformat(),
            "username": username_val if username_val else "Anonymous",
            "coordinates": {
                "latitude": latitude_val if latitude_val else None,
                "longitude": longitude_val if longitude_val else None
            },
            "category": category_val,
            "transcription_telugu": transcription,
            "translation_english": translation,
            "system_prompt": prompt_text
        }
        file_path = f"data/{file_id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return file_id

    # --- Translate Button ---
    if st.button("🌐 Translate to English using Gemini", use_container_width=True, type="primary"):
        # Construct the prompt for Gemini API
        prompt_for_gemini = f"""You are a professional translator. Translate the following Telugu text into fluent, natural English. Ensure the meaning, tone, and context are preserved. The input corpus might contain a mix of other languages and grammatical errors. Focus on the essence of the content. Do not display any header or footer, only the translated story.

Telugu:
\"\"\"{st.session_state.telugu_text.strip()}\"\"\""""

        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt_for_gemini}
                    ]
                }
            ]
        }

        try:
            with st.spinner("Translating with Gemini AI..."):
                response = requests.post(
                    f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
                    headers=headers,
                    json=payload,
                    timeout=20 # Increased timeout for API call
                )
                response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
                
                # Parse the JSON response
                response_json = response.json()
                
                # Extract the translated text, handling potential missing keys
                if "candidates" in response_json and len(response_json["candidates"]) > 0 and \
                   "content" in response_json["candidates"][0] and \
                   "parts" in response_json["candidates"][0]["content"] and \
                   len(response_json["candidates"][0]["content"]["parts"]) > 0:
                    translation = response_json["candidates"][0]["content"]["parts"][0]["text"]
                    st.session_state.translated_text = translation
                    st.success("✅ Translation completed!")

                    # Save the data
                    file_id = save_data(
                        transcription=st.session_state.telugu_text,
                        translation=translation,
                        prompt_text=prompt_for_gemini,
                        username_val=username,
                        latitude_val=latitude,
                        longitude_val=longitude,
                        category_val=category
                    )
                    st.info(f"📁 Data saved as `data/{file_id}.json`")
                else:
                    st.error("Gemini API response did not contain expected translation.")
                    st.json(response_json) # Display the full response for debugging

        except requests.exceptions.RequestException as req_err:
            st.error(f"Network or API request error: {req_err}")
        except json.JSONDecodeError as json_err:
            st.error(f"Failed to parse Gemini API response: {json_err}. Response: {response.text}")
        except Exception as e:
            st.error(f"An unexpected error occurred during translation: {e}")

# Display translation (if available)
if st.session_state.translated_text:
    st.text_area("🌍 English Translation", st.session_state.translated_text, height=250, disabled=True)

st.markdown("---")
st.markdown("Developed with ❤️ by Dev_404")
