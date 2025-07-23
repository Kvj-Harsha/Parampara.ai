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
st.set_page_config(page_title="Gemini Audio STT + Translation + Summary", layout="centered")

st.title("Parampara AI: Audio Transcription, Translation & Summary")
st.markdown("""
Upload a short audio clip (10–30 seconds) in **any Indic language**.

🧠 **Gemini (Google AI)** will transcribe it in the original language, translate it to **English**, and then generate a **structured summary**.

> ✅ All done with a single Gemini API call (transcription + translation + summary)!
""")

# --- Session State Initialization ---
if "original_lang_text" not in st.session_state:
    st.session_state.original_lang_text = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "summary_data" not in st.session_state:
    st.session_state.summary_data = None # Will store dict {title, category, instructions}

# --- User Metadata Section (using st.expander for a cleaner look) ---
with st.expander("🧾 Additional Information (Optional)", expanded=False):
    st.markdown("Provide optional details about the audio.")
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("👤 Your Name", key="username_input")
    with col2:
        category = st.selectbox("📁 Category", ["Story", "Interview", "News", "Tutorial: Pottery", "Other"], key="category_select")

    col3, col4 = st.columns(2)
    with col3:
        latitude = st.text_input("📍 Latitude", placeholder="e.g., 17.3850", key="latitude_input")
    with col4:
        longitude = st.text_input("📍 Longitude", placeholder="e.g., 78.4867", key="longitude_input")

# --- Language Selection Section ---
st.subheader("Language Selection")
# List of common Indic languages. You can expand this list as needed.
indic_languages = [
    "Hindi", "Bengali", "Marathi", "Telugu", "Tamil", "Gujarati",
    "Kannada", "Malayalam", "Punjabi", "Odia", "Assamese", "Urdu", "Nepali", "Konkani"
]
selected_language = st.selectbox("Select the language of the audio file:", indic_languages, index=3) # Default to Telugu

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

    # --- Transcription & Translation & Summary Button ---
    if st.button("📝🌐✨ Process Audio with Gemini (Transcribe, Translate & Summarize)", use_container_width=True, type="primary"):
        if temp_path: # Ensure temp_path exists before processing
            audio_data = None # Initialize audio_data here for finally block
            try:
                start_time = time.time()
                with st.spinner("Processing audio with Gemini AI (transcribing, translating & summarizing)... This might take a moment."):
                    st.info(f"Attempting to upload audio file from temp_path: {temp_path}")
                    audio_data = genai.upload_file(temp_path)
                    
                    if not audio_data or not audio_data.name:
                        st.error("Failed to upload audio file to Gemini. 'audio_data' is invalid or upload failed.")
                        # Raise a ValueError to be caught by the outer try-except block
                        raise ValueError("Gemini file upload failed.")

                    st.info(f"Audio file successfully uploaded to Gemini. File Name: {audio_data.name}, URI: {audio_data.uri}")

                    # Construct the prompt for Gemini API - Adjusted to match Gemini's actual output format
                    # Dynamically insert the selected_language here
                    prompt_for_gemini = f"""Please transcribe the following audio in {selected_language}. Then, translate the {selected_language} transcription into fluent, natural English.
                    Finally, analyze the English translation and provide a structured summary in JSON format.
                    If the content is a tutorial (e.g., pottery), structure the summary with a "title", a "category" (e.g., "Pottery Tutorial"), and an "instructions" array where each element is a numbered step.
                    If it's not a tutorial, provide a "title", a "category" (e.g., "General Summary"), and a "summary_text" field.
                    Ensure the meaning, tone, and context are preserved throughout. The input corpus might contain a mix of other languages and grammatical errors. Focus on the essence of the content.

                    Format your full response clearly as follows, including the markdown bolding and newlines:

                    **{selected_language} Transcription:**
                    [{selected_language} Transcribed Text Here]

                    **English Translation:**
                    [Translated English Text Here]

                    **Summary JSON:**
                    ```json
                    {{
                      "title": "Summary Title",
                      "category": "Pottery Tutorial" or "General Summary",
                      "instructions": [
                        "1. First step...",
                        "2. Second step...",
                        ...
                      ]
                    }}
                    ```
                    OR
                    ```json
                    {{
                      "title": "Summary Title",
                      "category": "General Summary",
                      "summary_text": "A concise summary of the content."
                    }}
                    ```
                    """
                    st.info("Sending request to Gemini model...")
                    response = model.generate_content([
                        {"role": "user", "parts": [
                            {"text": prompt_for_gemini},
                            audio_data # The audio file content
                        ]}
                    ])
                    st.info("Received response from Gemini model.")

                full_response_text = response.text
                duration = time.time() - start_time
                st.success(f"✅ Processing completed in {duration:.2f} seconds!")
                st.markdown("---")
                st.subheader("Raw Gemini API Response (for debugging):")
                st.text(full_response_text)
                st.markdown("---")


                # Parse the response to extract Telugu, English, and JSON summary parts
                # Adjusted prefixes to precisely match Gemini's output format
                original_lang_prefix_marker = f"**{selected_language} Transcription:**" # Dynamic prefix
                english_prefix_marker = "**English Translation:**"
                summary_json_block_start_marker = "```json" # This is the crucial marker for the JSON content itself
                summary_json_block_end_marker = "```"

                # Find the markers
                original_lang_start_idx = full_response_text.find(original_lang_prefix_marker)
                english_start_idx = full_response_text.find(english_prefix_marker)
                json_block_start_idx = full_response_text.find(summary_json_block_start_marker)
                json_block_end_idx = full_response_text.find(summary_json_block_end_marker, json_block_start_idx + len(summary_json_block_start_marker))

                st.info(f"Parsing indices: original_lang_start_idx={original_lang_start_idx}, english_start_idx={english_start_idx}, json_block_start_idx={json_block_start_idx}, json_block_end_idx={json_block_end_idx}")

                # Ensure all markers are found and in a logical order
                if (original_lang_start_idx != -1 and
                    english_start_idx != -1 and
                    json_block_start_idx != -1 and
                    json_block_end_idx != -1 and
                    original_lang_start_idx < english_start_idx < json_block_start_idx):
                    
                    # Extract original language text: from after its marker to before English marker, stripping newlines
                    original_lang_text_raw = full_response_text[original_lang_start_idx + len(original_lang_prefix_marker):english_start_idx].strip()
                    st.session_state.original_lang_text = original_lang_text_raw.strip() 

                    # Extract English text: from after its marker to before JSON block marker, stripping newlines
                    translated_text_raw = full_response_text[english_start_idx + len(english_prefix_marker):json_block_start_idx].strip()
                    st.session_state.translated_text = translated_text_raw.strip()

                    # Extract JSON string
                    json_string = full_response_text[json_block_start_idx + len(summary_json_block_start_marker):json_block_end_idx].strip()
                    try:
                        st.session_state.summary_data = json.loads(json_string)
                        st.success("✅ Transcription, Translation, and Summary extracted and parsed successfully!")
                    except json.JSONDecodeError as e:
                        st.error(f"Failed to parse Summary JSON. JSONDecodeError: {e}")
                        st.text(f"Attempted to parse this JSON string:\n```json\n{json_string}\n```") # Display malformed JSON for debugging
                        st.session_state.summary_data = None
                else:
                    st.error("Gemini API response did not contain all expected sections in the correct order, or parsing markers were not found. This means parsing failed.")
                    st.info("Please examine the 'Raw Gemini API Response' above and the 'Parsing indices' to understand why.")
                    st.session_state.original_lang_text = ""
                    st.session_state.translated_text = ""
                    st.session_state.summary_data = None


                # --- Save Data Function ---
                def save_data(transcription_original_lang, translation, summary, system_prompt, username_val, latitude_val, longitude_val, category_val, selected_lang_val):
                    """Saves transcription, translation, and summary data to a JSON file."""
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
                        "original_language": selected_lang_val, # Save the selected language
                        "transcription_original_language": transcription_original_lang,
                        "translation_english": translation,
                        "summary_data": summary, # Add summary data here
                        "system_prompt": system_prompt
                    }
                    file_path = f"data/{file_id}.json"
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    return file_id

                # Save the data
                if st.session_state.original_lang_text and st.session_state.translated_text and st.session_state.summary_data:
                    file_id = save_data(
                        transcription_original_lang=st.session_state.original_lang_text,
                        translation=st.session_state.translated_text,
                        summary=st.session_state.summary_data,
                        system_prompt=prompt_for_gemini, # Use the prompt sent to Gemini
                        username_val=username,
                        latitude_val=latitude,
                        longitude_val=longitude,
                        category_val=category,
                        selected_lang_val=selected_language # Pass the selected language
                    )
                    st.info(f"📁 Data saved as `data/{file_id}.json`")
                else:
                    st.warning("Could not save data due to missing transcription, translation, or summary after successful API call and parsing attempt. Check logs for details.")

            except ValueError as ve:
                st.error(f"A critical error occurred: {ve}")
            except Exception as e:
                st.error(f"An unexpected error occurred during Gemini processing: {e}")
                st.exception(e) # Display full traceback for debugging
            finally:
                # Clean up the temporary file and uploaded audio file
                if temp_path and os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                        st.info(f"Cleaned up local temporary audio file: {temp_path}")
                    except Exception as e:
                        st.warning(f"Could not delete local temporary file {temp_path}: {e}")
                
                # Clean up the uploaded file from Gemini's storage
                # Ensure audio_data is defined and has a name before attempting to delete
                if audio_data and audio_data.name:
                    try:
                        genai.delete_file(audio_data.name)
                        st.info(f"Cleaned up temporary Gemini uploaded file: {audio_data.name}")
                    except Exception as e:
                        st.warning(f"Could not delete Gemini uploaded file {audio_data.name}: {e}")
                else:
                    st.info("No Gemini uploaded file to clean up (or upload failed).")
        else:
            st.warning("Please upload an audio file first before clicking the process button.")

# --- Display Transcription and Translation Sections ---
if st.session_state.original_lang_text:
    st.subheader(f"📝 {selected_language} Transcript")
    st.text_area(f"{selected_language} Transcript", st.session_state.original_lang_text, height=180, disabled=True)

if st.session_state.translated_text:
    st.subheader("🌍 English Translation")
    st.text_area("English Translation", st.session_state.translated_text, height=250, disabled=True)

# --- Display Summary Section ---
if st.session_state.summary_data:
    st.subheader("✨ Summary")
    summary = st.session_state.summary_data
    
    if summary.get("title"):
        st.markdown(f"**Title:** {summary['title']}")
    
    if summary.get("category"):
        st.markdown(f"**Category:** {summary['category']}")
        
    if summary.get("instructions"):
        st.markdown("**Instructions:**")
        for i, instruction in enumerate(summary["instructions"]):
            # Display instructions with proper numbering, even if not provided by Gemini in the string
            st.markdown(f"{i+1}. {instruction.lstrip(f'{i+1}. ').strip()}") # Removes potential "1." from start
    elif summary.get("summary_text"):
        st.markdown("**Summary:**")
        st.markdown(summary["summary_text"])
    else:
        st.warning("Summary data found, but unexpected format or empty. Displaying raw JSON for debug:")
        st.json(summary) # Show raw JSON for debugging

st.markdown("---")
st.markdown("Developed with ❤️ by Dev_404")