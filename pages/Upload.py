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

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY not found. Please set it in your .env file.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="Gemini Audio STT + Translation + Summary", layout="centered")
st.title("Parampara AI: Audio Transcription, Translation & Summary")
st.markdown("""
Upload a short audio clip (10–30 seconds) in **any Indic language**.
🧠 **Gemini (Google AI)** will transcribe it in the original language, translate it to **English**, and then generate a **structured summary**.
""")

if "original_lang_text" not in st.session_state:
    st.session_state.original_lang_text = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "summary_data" not in st.session_state:
    st.session_state.summary_data = None

with st.expander("🧾 Additional Information (Optional)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("👤 Your Name")
    with col2:
        category = st.selectbox("📁 Category", ["Story", "Interview", "News", "Tutorial: Pottery", "Other"])
    col3, col4 = st.columns(2)
    with col3:
        latitude = st.text_input("📍 Latitude", placeholder="e.g., 17.3850")
    with col4:
        longitude = st.text_input("📍 Longitude", placeholder="e.g., 78.4867")

st.subheader("Language Selection")
indic_languages = [
    "Hindi", "Bengali", "Marathi", "Telugu", "Tamil", "Gujarati",
    "Kannada", "Malayalam", "Punjabi", "Odia", "Assamese", "Urdu", "Nepali", "Konkani"
]
selected_language = st.selectbox("Select the language of the audio file:", indic_languages, index=3)

st.subheader("Upload Media")
audio_file = st.file_uploader("📤 Upload an audio file", type=["mp3", "wav", "m4a", "mp4"])
image_files = st.file_uploader("🖼 Upload image(s)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
video_files = st.file_uploader("🎞 Upload video(s)", type=["mp4", "mov", "avi"], accept_multiple_files=True)
doc_files = st.file_uploader("📄 Upload document(s)", type=["pdf", "docx", "txt"], accept_multiple_files=True)

def save_uploaded_file(upload, subfolder):
    if upload is None:
        return None
    os.makedirs(f"data/uploads/{subfolder}", exist_ok=True)
    file_id = f"{uuid.uuid4()}{pathlib.Path(upload.name).suffix}"
    dest = f"data/uploads/{subfolder}/{file_id}"
    with open(dest, "wb") as out_file:
        out_file.write(upload.read())
    return dest

if st.button("📝🌐✨ Process Audio with Gemini (Transcribe, Translate & Summarize)", use_container_width=True, type="primary"):
    temp_path = None
    audio_data = None
    try:
        if audio_file:
            ext = pathlib.Path(audio_file.name).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_audio:
                temp_audio.write(audio_file.read())
                temp_path = temp_audio.name
                st.audio(temp_path)
                with st.spinner("Processing audio with Gemini..."):
                    audio_data = genai.upload_file(temp_path)
                    prompt = f"""Please transcribe the following audio in {selected_language}. Then, translate the {selected_language} transcription into fluent, natural English...

**{selected_language} Transcription:**
[...]
**English Translation:**
[...]
**Summary JSON:**
```json
{{}}
```
"""
                    response = model.generate_content([
                        {"role": "user", "parts": [
                            {"text": prompt},
                            audio_data
                        ]}
                    ])
            text = response.text
            orig_start = text.find(f"**{selected_language} Transcription:**")
            trans_start = text.find("**English Translation:**")
            json_start = text.find("```json")
            json_end = text.find("```", json_start + 7)

            if orig_start != -1 and trans_start != -1 and json_start != -1 and json_end != -1:
                orig_text = text[orig_start + len(f"**{selected_language} Transcription:**"):trans_start].strip()
                trans_text = text[trans_start + len("**English Translation:**"):json_start].strip()
                json_str = text[json_start + 7:json_end].strip()
                try:
                    summary_data = json.loads(json_str)
                except:
                    summary_data = None

                st.session_state.original_lang_text = orig_text
                st.session_state.translated_text = trans_text
                st.session_state.summary_data = summary_data

        image_paths = [save_uploaded_file(f, "image") for f in image_files if f is not None]
        video_paths = [save_uploaded_file(f, "video") for f in video_files if f is not None]
        file_paths = [save_uploaded_file(f, "file") for f in doc_files if f is not None]

        os.makedirs("data/records", exist_ok=True)
        file_id = str(uuid.uuid4())
        record = {
            "id": file_id,
            "timestamp": datetime.now().isoformat(),
            "username": username or "Anonymous",
            "coordinates": {
                "latitude": latitude or None,
                "longitude": longitude or None
            },
            "category": category,
            "original_language": selected_language,
            "transcription_original_language": st.session_state.original_lang_text or None,
            "translation_english": st.session_state.translated_text or None,
            "summary_data": st.session_state.summary_data,
            "system_prompt": prompt if audio_file else None,
            "media": {
                "audio_url": save_uploaded_file(audio_file, "audio") if audio_file else None,
                "image_urls": image_paths,
                "video_urls": video_paths,
                "file_urls": file_paths
            }
        }
        with open(f"data/{file_id}.json", "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        st.success(f"✅ Saved record to data/records/{file_id}.json")

    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        if audio_data and hasattr(audio_data, "name"):
            try:
                genai.delete_file(audio_data.name)
            except:
                pass

if st.session_state.original_lang_text:
    st.subheader(f"📝 {selected_language} Transcript")
    st.text_area(f"{selected_language} Transcript", st.session_state.original_lang_text, height=180, disabled=True)

if st.session_state.translated_text:
    st.subheader("🌍 English Translation")
    st.text_area("English Translation", st.session_state.translated_text, height=250, disabled=True)

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
            st.markdown(f"{i+1}. {instruction.lstrip(f'{i+1}. ').strip()}")
    elif summary.get("summary_text"):
        st.markdown("**Summary:**")
        st.markdown(summary["summary_text"])
    else:
        st.json(summary)

st.markdown("---")
st.markdown("Developed with ❤️ by Dev_404")
