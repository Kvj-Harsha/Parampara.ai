import gradio as gr
import openai
from googletrans import Translator
import os

# 🔐 Load API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
translator = Translator()

# 🎧 Transcription using OpenAI Whisper API
def transcribe_translate(audio):
    with open(audio, "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f)["text"]
    translation = translator.translate(transcript, src='en', dest='hi').text
    return transcript, translation

# 🧠 Tutorial generation using GPT-4
def generate_tutorial(text):
    prompt = f"Generate a clear step-by-step tutorial from this artisan's description:\n\n{text}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

# 💬 Cultural chatbot
def ask_chatbot(question):
    prompt = f"Answer this cultural question related to traditional skills and crafts:\n{question}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

# 🎛 Gradio UI
with gr.Blocks(title="Parampara.ai – Preserve Skills with AI") as app:
    gr.Markdown("## 🪔 Parampara.ai – Preserving Traditional Knowledge with AI")

    with gr.Tab("🎧 Transcribe + Translate"):
        audio = gr.Audio(type="filepath", label="Upload Audio or Video")
        transcript = gr.Textbox(label="Transcript")
        translated = gr.Textbox(label="Translation (Hindi)")
        trans_btn = gr.Button("Transcribe & Translate")
        trans_btn.click(fn=transcribe_translate, inputs=audio, outputs=[transcript, translated])

    with gr.Tab("📚 Generate Tutorial"):
        tutorial_input = gr.Textbox(label="Paste Transcript or Description", lines=6)
        tutorial_output = gr.Textbox(label="Generated Tutorial", lines=6)
        tutorial_btn = gr.Button("Generate Tutorial")
        tutorial_btn.click(fn=generate_tutorial, inputs=tutorial_input, outputs=tutorial_output)

    with gr.Tab("💬 Ask Cultural Chatbot"):
        question = gr.Textbox(label="Ask about a craft, tradition, or artisan")
        answer = gr.Textbox(label="Chatbot Answer")
        chat_btn = gr.Button("Ask")
        chat_btn.click(fn=ask_chatbot, inputs=question, outputs=answer)

app.launch()
