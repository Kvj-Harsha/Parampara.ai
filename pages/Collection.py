import streamlit as st
import json
from datetime import datetime
import os
import glob # Import glob to find files matching a pattern

st.set_page_config(page_title="JSON Data Viewer", layout="centered")

st.title("📄 JSON Data Viewer")
st.markdown("This page allows you to browse and display details from JSON files stored in the `data/` directory. "
            "It supports the transcription, translation, and structured summary output from the Gemini Audio App.")

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
    # Sort files by modification time, newest first, for easier Browse of recent entries
    json_files = sorted(glob.glob(os.path.join(data_dir, "*.json")), key=os.path.getmtime, reverse=True)
else:
    st.warning(f"The directory '{data_dir}' does not exist. Please create it and place your JSON files inside.")

# --- File Selection Dropdown ---
selected_file = None
data = None # Initialize data outside the if-else for wider scope

if json_files:
    # Present file names with a more user-friendly format (e.g., ID and timestamp if available)
    file_options = []
    for f_path in json_files:
        temp_data = load_json_data(f_path)
        if temp_data:
            file_id = temp_data.get("id", "N/A")[:8] # Shorten ID for display
            timestamp_str = temp_data.get("timestamp")
            display_timestamp = "Unknown Date"
            if timestamp_str:
                try:
                    # Attempt to parse ISO format first, then basic strptime if that fails
                    timestamp_dt = datetime.fromisoformat(timestamp_str)
                    display_timestamp = timestamp_dt.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    try:
                        timestamp_dt = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%f")
                        display_timestamp = timestamp_dt.strftime("%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        display_timestamp = timestamp_str # Fallback to raw string
            file_options.append(f"{display_timestamp} - ID: {file_id} ({os.path.basename(f_path)})")
        else:
            file_options.append(f"Error reading: {os.path.basename(f_path)}")

    selected_option = st.selectbox("Select a JSON entry to view:", file_options)
    if selected_option and "ID: " in selected_option:
        # Extract the original file path from the selected option
        original_file_name = selected_option.split('(')[-1].rstrip(')')
        selected_file = os.path.join(data_dir, original_file_name)
        data = load_json_data(selected_file)
else:
    st.info("No JSON files found in the 'data/' directory. Please upload or create some using the main app.")

# --- Display Data ---
if data:
    st.subheader("📋 General Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("ID", data.get("id", "N/A"))
    with col2:
        timestamp_str = data.get("timestamp")
        timestamp_dt_formatted = "N/A"
        if timestamp_str:
            try:
                # Handle potential timezone info if present, or just parse without it
                # datetime.fromisoformat handles optional timezone and microseconds well
                timestamp_dt = datetime.fromisoformat(timestamp_str)
                # Format to a readable string, considering local time zone (not strictly necessary as it's just display)
                timestamp_dt_formatted = timestamp_dt.strftime("%Y-%m-%d %H:%M:%S %Z") # %Z for timezone name if available
            except ValueError:
                # Fallback for older formats if fromisoformat fails
                try:
                    timestamp_dt = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%f")
                    timestamp_dt_formatted = timestamp_dt.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    timestamp_dt_formatted = timestamp_str # Fallback to raw string if parsing fails
        st.metric("Timestamp", timestamp_dt_formatted)
    with col3:
        st.metric("Username", data.get("username", "Anonymous")) # Default to Anonymous

    st.subheader("🗂️ Categorization & Location")
    col4, col5 = st.columns(2)
    with col4:
        st.metric("Category", data.get("category", "Uncategorized")) # Default to Uncategorized
    with col5:
        coords = data.get("coordinates", {})
        latitude = coords.get("latitude")
        longitude = coords.get("longitude")
        
        display_lat = latitude if latitude is not None and latitude != "" else "N/A"
        display_lon = longitude if longitude is not None and longitude != "" else "N/A"
        st.metric("Coordinates", f"Lat: {display_lat}, Lon: {display_lon}")

    st.subheader("🗣️ Transcription and Translation")
    st.text_area("📝 Telugu Transcription", data.get("transcription_telugu", "No Telugu transcription available."), height=200, disabled=True)
    st.text_area("🌍 English Translation", data.get("translation_english", "No English translation available."), height=300, disabled=True)

    # --- New Summary Section ---
    st.subheader("✨ Summary")
    summary_data = data.get("summary_data")

    if summary_data:
        summary_title = summary_data.get("title", "No Title Provided")
        summary_category = summary_data.get("category", "General Summary")
        instructions = summary_data.get("instructions")
        summary_text = summary_data.get("summary_text")

        st.markdown(f"**Summary Title:** {summary_title}")
        st.markdown(f"**Summary Category:** {summary_category}")

        if instructions:
            st.markdown("---")
            st.markdown("#### Instructions/Steps:")
            for i, step in enumerate(instructions):
                st.markdown(f"**{i+1}.** {step.strip()}") # Ensure clean display of steps
        elif summary_text:
            st.markdown("---")
            st.markdown("#### Detailed Summary:")
            st.markdown(summary_text)
        else:
            st.warning("Summary data found, but it does not contain 'instructions' or 'summary_text' fields.")
            with st.expander("View Raw Summary Data"):
                st.json(summary_data)
    else:
        st.info("No structured summary data found for this entry.")

    with st.expander("⚙️ System Prompt Used for Gemini API"):
        st.code(data.get("system_prompt", "No system prompt recorded."), language="text")

    st.subheader("💡 Raw JSON Data")
    with st.expander("View Full Raw JSON"):
        st.json(data)
else:
    if selected_file: # Only show this warning if a file was selected but couldn't be loaded
        st.warning("Failed to load data from the selected file. It might be corrupted or malformed JSON.")
    # The message for no files found is handled earlier

st.markdown("---")
st.markdown("Developed with ❤️ by Dev_404")
st.markdown(f"Current server time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}") # Display current time for context
st.markdown("Location: Secunderabad, Telangana, India")