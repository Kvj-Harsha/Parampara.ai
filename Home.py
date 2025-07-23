import streamlit as st
from PIL import Image # Keep Image import if you plan to use a logo later

# Optional: Set page config
st.set_page_config(page_title="Parampara AI", page_icon="🧠", layout="wide")

# --- Header Section ---
# Use columns for better alignment of title and potentially a logo
col1, col2 = st.columns([0.7, 0.3]) # Adjust column ratio as needed for a logo
with col1:
    st.title("Parampara AI")
    st.markdown("<h3 style='color: #6A057F;'>Bridging Tradition with Modern AI</h3>", unsafe_allow_html=True) # Tagline with custom color
# with col2:
    # You can add a logo here if you have one
    # try:
    #     logo = Image.open("path/to/your/logo.png") # Replace with your logo path
    #     st.image(logo, width=150)
    # except FileNotFoundError:
    #     pass # Handle if logo is not found

st.markdown("---") # Visual separator

# --- Introduction Section ---
st.markdown("### Welcome to Parampara AI")
st.write("""
Parampara AI is an intelligent platform designed to blend the wisdom of ancient traditions with the power of modern artificial intelligence. 
We empower artisans and knowledge keepers to preserve, document, and share their invaluable heritage with the world.
""")

st.markdown("---") # Visual separator

# --- Key Features/Value Proposition (Concise) ---
st.markdown("### How We Help:")
st.write("""
* **Preserve Oral Traditions:** Transcribe and translate audio and video content from local languages.
* **Structure Knowledge:** Convert rich, unstructured traditional knowledge into searchable, organized data.
* **Global Reach:** Make unique artisanal practices and stories accessible to a worldwide audience.
""")

st.markdown("---") # Visual separator

# --- Call to Action (CTAs) ---
st.markdown("## 👇 Explore Our Tools")

st.write("Ready to transform your traditional knowledge? Choose an option below to get started:")

col_buttons1, col_buttons2 = st.columns(2)

with col_buttons1:
    st.page_link("pages/upload.py", label="🗣️ Transcribe & Translate Audio", icon="🔊")

with col_buttons2:
    st.page_link("pages/collection.py", label="📄 View Your Data Collection", icon="📁")


st.markdown("<br>", unsafe_allow_html=True) # Add some space

# Optional: More engaging message if using a sidebar for navigation (common in multi-page apps)
# If this is the main app, and you have pages defined as .py files in a 'pages' folder,
# Streamlit automatically creates the sidebar navigation.
# If not, you'd guide them to buttons as above.
# st.success("Or, use the sidebar on the left to navigate between different features.")


# --- Footer ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>© 2025 Parampara AI. All rights reserved.</p>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; color: gray; font-size: small;'>Bridging the Past and the Future | ❤️ se India</p>",
    unsafe_allow_html=True
)