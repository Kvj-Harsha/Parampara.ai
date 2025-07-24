# 🧠 Parampara AI  
**Bridging Tradition with Modern AI**  
[🌐 Live Demo → **parampara.streamlit.app**](https://parampara.streamlit.app)

> ⚠️ *Note: Open-source speech/translation models were considered and tested locally. However, due to the cost and complexity of deploying them, we used Google's Gemini API in the deployed version.*

---

## 📌 Overview

**Parampara AI** is a Streamlit-based platform designed to help preserve oral and cultural traditions. It enables **knowledge keepers, artisans, and storytellers**—especially from rural and indigenous communities—to digitize their spoken narratives and craft knowledge.

Using **Google's Gemini AI**, it transcribes, translates, and summarizes audio inputs (in Indian languages like **Telugu**) into structured, accessible digital formats.

---

## 🚀 Key Features

- 🎙️ **Transcribe & Translate**  
  Converts spoken audio in regional languages like Telugu to English text.

- 🧠 **AI-Powered Summarization**  
  Generates structured, step-by-step instructions or narrative summaries.

- 🌍 **Metadata Enrichment**  
  Captures contextual info: speaker name, location, and category.

- 📁 **Collection View**  
  Easily browse past uploads with access to audio, transcript, translation, and summaries.

---

## 🧱 System Architecture & Workflow

![System Architecture](https://res.cloudinary.com/dtqhbvndz/image/upload/v1753257388/archi_iwj7lm.png)

---

## 📂 Project Structure

```
ParamparaAI/
├── .venv/                      # Virtual environment (excluded via .gitignore)
├── data/                       # Auto-saved summaries and metadata (JSON files)
├── pages/
│   ├── Collection.py           # View uploaded data and summaries
│   └── Upload.py               # Audio upload and processing interface
├── .env                        # API keys (Gemini API)
├── .gitignore
├── Home.py                     # Main homepage and UI
├── README.md                   # Project documentation
├── requirements.txt            # Required Python packages
├── test.wav                    # Sample test audio
```

---

## 🧑‍💻 Getting Started Locally

1. **Clone the Repository**

```bash
git clone https://github.com/your-org/parampara-ai.git
cd parampara-ai
```

2. **Install Requirements**

```bash
pip install -r requirements.txt
```

3. **Set Up API Key**

Create a `.env` file with your Google Gemini API key:

```env
GEMINI_API_KEY=your_google_gemini_api_key
```

4. **Run the App**

```bash
streamlit run Home.py
```

---

## ⚙️ Tech Stack & Dependencies

- **Python 3.8+**
- **Streamlit** – For interactive UI
- **Google Generative AI (Gemini)** – For transcription, translation, summarization
- **dotenv**, **Pillow**, **uuid**, etc.

---

## 🧪 Notes on Models & Hosting

🔍 **Open-Source Model Note**  
The project initially explored using **open-source speech-to-text and translation models**. While these models performed well locally during testing (offline and downloaded), **hosting them proved cost-prohibitive** for deployment. Therefore, for scalability and quick integration, **Google Gemini API** was used during deployment.

---

## 💡 Example Use Case

> 🎧 A 20-60 second or more audio clip of a Telugu-speaking artisan describing traditional pottery is uploaded.  
> Parampara AI:
> - Transcribes the Telugu audio.
> - Translates it into English.
> - Generates a clear, step-by-step tutorial for documentation and learning.

---

## 🙌 Credits

> 🛠️ Developed by **Team Dev_404** — Interns at **VISWAM.AI** — as part of the **SoAI Program** organized by [**VISWAM.AI**](https://viswam.ai) & [**Swecha**](https://swecha.org).

---

## 📄 License

MIT License – Use, modify, and share freely with attribution.