import streamlit as st
import openai
from googletrans import Translator
from dotenv import load_dotenv
import os

# Load environment variables (API keys)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Translator setup
translator = Translator()

# App config
st.set_page_config(page_title="Parampara.ai", layout="wide")
st.title("🪔 Parampara.ai – Preserving Artisan Wisdom with AI")
st.markdown("Upload craft videos, generate tutorials, and explore cultural knowledge using AI.")

# Section 1: Transcribe & Translate
st.header("🎧 Step 1: Upload Artisan Audio/Video for Transcription & Translation")
audio_file = st.file_uploader("Upload an audio or video file (mp3, mp4, wav, m4a)", type=["mp3", "mp4", "wav", "m4a"])

if audio_file and st.button("Transcribe & Translate"):
    with st.spinner("Transcribing using Whisper API..."):
        transcript = openai.Audio.transcribe("whisper-1", audio_file)["text"]
        st.success("Transcript generated:")
        st.text_area("Transcript (English)", transcript, height=200)

        with st.spinner("Translating to Hindi..."):
            translated = translator.translate(transcript, src='en', dest='hi').text
            st.success("Translation complete:")
            st.text_area("अनुवाद (Translation in Hindi)", translated, height=200)

# Section 2: Tutorial Generation
st.header("📚 Step 2: Generate Step-by-Step Tutorial from Transcript")
tutorial_input = st.text_area("Paste the transcript or artisan's description here", height=200)
if st.button("Generate Tutorial"):
    with st.spinner("Generating tutorial using GPT-4..."):
        prompt = f"Create a clear, step-by-step tutorial from this artisan's description:\n\n{tutorial_input}\n\nSteps:"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        tutorial = response.choices[0].message["content"]
        st.success("Tutorial generated:")
        st.text_area("Tutorial", tutorial, height=300)

# Section 3: Cultural Chatbot Q&A
st.header("💬 Step 3: Ask a Cultural or Craft-related Question")
user_question = st.text_input("What would you like to know? (e.g., 'Why do artisans soak bamboo before weaving?')")
if st.button("Ask the Chatbot"):
    with st.spinner("Getting answer from GPT-4..."):
        prompt = f"You are an expert in Indian traditional crafts. Answer this question with cultural and practical insight:\n\n{user_question}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )
        answer = response.choices[0].message["content"]
        st.success("Response:")
        st.text_area("Chatbot Answer", answer, height=200)
