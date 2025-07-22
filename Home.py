import streamlit as st
from PIL import Image

# Optional: Set page config
st.set_page_config(page_title="Parampara AI", page_icon="🧠", layout="wide")

# Title & Tagline
st.title("Parampara AI")
st.subheader("Bridging Tradition with Modern AI")

st.markdown("---")

# Intro Section
st.markdown("### Welcome to Parampara AI")
st.write("""
Parampara AI is an intelligent platform designed to blend the wisdom of traditions with the power of modern artificial intelligence. 
Whether you're enhancing decision-making, preserving knowledge, or building smarter tools — Parampara AI is your trusted companion on the journey to innovation with roots.
""")


# CTA Section
st.markdown("---")
st.markdown("## 👇 Get Started")
st.write("Use the sidebar to navigate through the platform and explore the tools and features available.")

st.success("👈 Choose a page from the sidebar to begin your journey.")

# Optional footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>© 2025 Parampara AI · Bridging the Past and the Future</p>",
    unsafe_allow_html=True
)
# Sidebar navigation