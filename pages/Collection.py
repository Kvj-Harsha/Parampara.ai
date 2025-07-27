import streamlit as st
import json
from datetime import datetime
import os
import glob

st.set_page_config(page_title="JSON Data Viewer", layout="centered")

st.title("Parampara AI: Data Collection Viewer")
st.markdown("This page allows you to browse and display details from JSON files stored in the `data/` directory. "
            "It supports the transcription, translation, and structured summary output from the Gemini Audio App.")

# --- Function to load data from a specific file ---
def load_json_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Failed to read JSON file: {e}")
        return None

# --- Find all JSON files in the 'data' directory ---
data_dir = "data"
json_files = sorted(glob.glob(os.path.join(data_dir, "*.json")), key=os.path.getmtime, reverse=True)

selected_file = None
data = None

if json_files:
    file_options = []
    for f_path in json_files:
        temp_data = load_json_data(f_path)
        if temp_data:
            file_id = temp_data.get("id", "N/A")[:8]
            timestamp_str = temp_data.get("timestamp")
            try:
                timestamp_dt = datetime.fromisoformat(timestamp_str)
                display_timestamp = timestamp_dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                display_timestamp = timestamp_str or "Unknown"
            file_options.append(f"{display_timestamp} - ID: {file_id} ({os.path.basename(f_path)})")

    selected_option = st.selectbox("Select a JSON entry to view:", file_options)
    if selected_option:
        selected_file = os.path.join(data_dir, selected_option.split("(")[-1].rstrip(")"))
        data = load_json_data(selected_file)
else:
    st.warning("No JSON files found in the 'data/' directory.")

if data:
    st.subheader("📋 General Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("ID", data.get("id", "N/A"))
    with col2:
        timestamp = data.get("timestamp", "N/A")
        try:
            timestamp_dt = datetime.fromisoformat(timestamp)
            timestamp = timestamp_dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            pass
        st.metric("Timestamp", timestamp)
    with col3:
        st.metric("Username", data.get("username", "Anonymous"))

    st.subheader("🗂️ Categorization & Location")
    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("Category", data.get("category", "Uncategorized"))
    with col5:
        coords = data.get("coordinates", {})
        st.metric("Coordinates", f"Lat: {coords.get('latitude', 'N/A')}, Lon: {coords.get('longitude', 'N/A')}")
    with col6:
        st.metric("Original Language", data.get("original_language", "N/A"))

    st.subheader("🗣️ Transcription and Translation")
    original_lang = data.get("original_language", "Original Language")
    st.text_area(f"📝 {original_lang} Transcription", data.get("transcription_original_language", "N/A"), height=200, disabled=True)
    st.text_area("🌍 English Translation", data.get("translation_english", "N/A"), height=250, disabled=True)

    st.subheader("✨ Summary")
    summary = data.get("summary_data")
    if summary:
        st.markdown(f"**Title:** {summary.get('title', 'N/A')}")
        st.markdown(f"**Category:** {summary.get('category', 'N/A')}")
        if summary.get("instructions"):
            st.markdown("**Instructions:**")
            for i, step in enumerate(summary["instructions"], 1):
                st.markdown(f"{i}. {step.strip()}")
        elif summary.get("summary_text"):
            st.markdown("**Summary:**")
            st.markdown(summary["summary_text"])
        else:
            st.info("Summary present but no detailed fields found.")
            st.json(summary)
    else:
        st.info("No structured summary found.")

    with st.expander("⚙️ System Prompt Used for Gemini API"):
        st.code(data.get("system_prompt", "No system prompt recorded."))

    st.subheader("📦 Uploaded Media")
    media = data.get("media", {})

    # Handle all plural list-based media fields
    for media_type, display_func in {
        "audio_urls": st.audio,
        "video_urls": st.video,
        "image_urls": st.image,
        "file_urls": lambda x: st.markdown(f"[📄 Download File]({x})")
    }.items():
        if media.get(media_type):
            for item in media[media_type]:
                display_func(item)
                if media_type != "file_urls":
                    st.caption(item)

    st.subheader("💡 Raw JSON Data")
    with st.expander("View Full Raw JSON"):
        st.json(data)

st.markdown("---")
st.markdown("Developed with ❤️ by Dev_404")
st.markdown(f"Current server time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.markdown("Location: Secunderabad, Telangana, India")
