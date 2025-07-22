import streamlit as st
import json
from datetime import datetime
import os
import glob # Import glob to find files matching a pattern

st.set_page_config(page_title="JSON Data Viewer", layout="centered")

st.title("📄 JSON Data Viewer")
st.markdown("This page allows you to browse and display details from JSON files stored in the `data/` directory.")

# --- Function to load data from a specific file ---
def load_json_data(file_path):
    """Loads JSON data from the given file path."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        st.error(f"Error: Could not decode JSON from {file_path}. Please check the file format.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred while reading {file_path}: {e}")
        return None

# --- Find all JSON files in the 'data' directory ---
data_dir = "data"
json_files = []
if os.path.exists(data_dir) and os.path.isdir(data_dir):
    json_files = sorted(glob.glob(os.path.join(data_dir, "*.json")))
else:
    st.warning(f"The directory '{data_dir}' does not exist. Please create it and place your JSON files inside.")

# --- File Selection Dropdown ---
selected_file = None
if json_files:
    file_names = [os.path.basename(f) for f in json_files]
    selected_file_name = st.selectbox("Select a JSON file to view:", file_names)
    if selected_file_name:
        selected_file = os.path.join(data_dir, selected_file_name)
else:
    st.info("No JSON files found in the 'data/' directory. Please upload or create some.")

data = None
if selected_file:
    data = load_json_data(selected_file)

if data:
    st.subheader("General Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("ID", data.get("id", "N/A"))
    with col2:
        timestamp_str = data.get("timestamp")
        timestamp_dt = "N/A"
        if timestamp_str:
            try:
                # Handle potential timezone info if present, or just parse without it
                if 'T' in timestamp_str and '+' in timestamp_str:
                    timestamp_dt = datetime.fromisoformat(timestamp_str)
                else:
                    timestamp_dt = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%f")
                timestamp_dt = timestamp_dt.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                timestamp_dt = timestamp_str # Fallback to raw string if parsing fails
        st.metric("Timestamp", timestamp_dt)
    with col3:
        st.metric("Username", data.get("username", "N/A"))

    st.subheader("Categorization")
    col4, col5 = st.columns(2)
    with col4:
        st.metric("Category", data.get("category", "N/A"))
    with col5:
        coords = data.get("coordinates", {})
        latitude = coords.get("latitude") if coords.get("latitude") is not None else "N/A"
        longitude = coords.get("longitude") if coords.get("longitude") is not None else "N/A"
        st.metric("Coordinates", f"Lat: {latitude}, Lon: {longitude}")

    st.subheader("Transcriptions and Translations")

    st.text_area("📝 Telugu Transcription", data.get("transcription_telugu", "N/A"), height=250, disabled=True)
    st.text_area("🌍 English Translation", data.get("translation_english", "N/A"), height=350, disabled=True)

    with st.expander("System Prompt Used for Translation"):
        st.code(data.get("system_prompt", "N/A"), language="text")

    st.subheader("Raw JSON Data")
    with st.expander("View Raw JSON"):
        st.json(data)
else:
    if selected_file: # Only show this warning if a file was selected but couldn't be loaded
        st.warning("Please select a JSON file from the dropdown above to display its content.")
    # The message for no files found is handled earlier

st.markdown("---")
st.markdown("This application demonstrates displaying structured JSON data in Streamlit.")
