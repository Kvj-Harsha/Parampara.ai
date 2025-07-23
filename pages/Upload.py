import streamlit as st
import tempfile
import time
import os
import json
import uuid
from datetime import datetime
import pathlib
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables (ensure .env file exists with GEMINI_API_KEY)
load_dotenv()

# --- CONFIG ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Ensure GEMINI_API_KEY is set
if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY not found. Please set it in your .env file.")
    st.stop()

# Configure the Gemini API with the API key
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model for audio processing
# Using gemini-1.5-flash which supports multimodal input including audio
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Gemini Audio STT + Translation", layout="centered")

st.title("🗣️ Gemini Audio STT + Translation – Telugu Audio to English")
st.markdown("""
Upload a short audio clip (10–30 seconds) in **Telugu**.

🧠 **Gemini (Google AI)** will transcribe it in Telugu and then translate it to **English**.

> ✅ All done with a single Gemini API call!
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

    # --- Transcription & Translation Button ---
    # The button now triggers both transcription and translation via Gemini
    if st.button("📝🌐 Transcribe & Translate Audio with Gemini", use_container_width=True, type="primary"):
        if temp_path: # Ensure temp_path exists before processing
            try:
                start_time = time.time()
                with st.spinner("Processing audio with Gemini AI (transcribing & translating)... This might take a moment."):
                    # Prepare the audio file for Gemini
                    audio_data = genai.upload_file(temp_path)

                    # Construct the prompt for Gemini API
                    # We ask Gemini to output both the Telugu transcription and English translation
                    prompt_for_gemini = """Please transcribe the following audio in Telugu and then translate the Telugu transcription into fluent, natural English. Ensure the meaning, tone, and context are preserved. The input corpus might contain a mix of other languages and grammatical errors. Focus on the essence of the content.

Format your response clearly as follows:
Telugu Transcription: [Transcribed Telugu Text Here]
English Translation: [Translated English Text Here]
"""
                    # Send audio and prompt to Gemini
                    response = model.generate_content([
                        {"role": "user", "parts": [
                            {"text": prompt_for_gemini},
                            audio_data # The audio file content
                        ]}
                    ])

                full_response_text = response.text
                duration = time.time() - start_time
                st.success(f"✅ Processing completed in {duration:.2f} seconds!")

                # Parse the response to extract Telugu and English parts
                telugu_prefix = "Telugu Transcription: "
                english_prefix = "English Translation: "

                telugu_start = full_response_text.find(telugu_prefix)
                english_start = full_response_text.find(english_prefix)

                if telugu_start != -1 and english_start != -1:
                    # Extract Telugu text
                    telugu_text_raw = full_response_text[telugu_start + len(telugu_prefix):english_start].strip()
                    st.session_state.telugu_text = telugu_text_raw

                    # Extract English text
                    translated_text_raw = full_response_text[english_start + len(english_prefix):].strip()
                    st.session_state.translated_text = translated_text_raw
                    
                    st.success("✅ Transcription and Translation extracted!")

                    # --- Save Data Function ---
                    def save_data(transcription, translation, system_prompt, username_val, latitude_val, longitude_val, category_val):
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
                            "system_prompt": system_prompt
                        }
                        file_path = f"data/{file_id}.json"
                        with open(file_path, "w", encoding="utf-8") as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                        return file_id

                    # Save the data
                    file_id = save_data(
                        transcription=st.session_state.telugu_text,
                        translation=st.session_state.translated_text,
                        system_prompt=prompt_for_gemini, # Use the prompt sent to Gemini
                        username_val=username,
                        latitude_val=latitude,
                        longitude_val=longitude,
                        category_val=category
                    )
                    st.info(f"📁 Data saved as `data/{file_id}.json`")

                else:
                    st.error("Gemini API response did not contain expected 'Telugu Transcription' or 'English Translation' sections. Raw response:")
                    st.text(full_response_text) # Display the full response for debugging

            except Exception as e:
                st.error(f"An error occurred during Gemini processing: {e}")
                st.exception(e) # Display full traceback for debugging
            finally:
                # Clean up the temporary file and uploaded audio file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                # Clean up the uploaded file from Gemini's storage
                if 'audio_data' in locals() and audio_data:
                    try:
                        genai.delete_file(audio_data.name)
                        st.info("Cleaned up temporary Gemini uploaded file.")
                    except Exception as e:
                        st.warning(f"Could not delete Gemini uploaded file: {e}")
        else:
            st.warning("Please upload an audio file first.")

# --- Display Transcription and Translation Sections ---
if st.session_state.telugu_text:
    st.subheader("Transcription & Translation")
    st.text_area("📝 Telugu Transcript", st.session_state.telugu_text, height=180, disabled=True)

if st.session_state.translated_text:
    st.text_area("🌍 English Translation", st.session_state.translated_text, height=250, disabled=True)

st.markdown("---")
st.markdown("Developed with ❤️ by Dev_404")
