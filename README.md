
# 🧠 Parampara AI

**Bridging Tradition with Modern AI**  
A Streamlit-based app to preserve and process oral traditions using Google's Gemini AI.

---

## 📌 Overview

**Parampara AI** is an intelligent platform that empowers knowledge keepers, artisans, and storytellers to preserve their cultural heritage. It uses **Google Gemini AI** to transcribe, translate, and summarize audio clips—especially in Indian languages like **Telugu**—into structured and accessible digital content.

---

## 🚀 Features

- 🎙️ **Transcribe & Translate**: Converts spoken audio in Telugu into English text.
- 🧠 **Structured Summaries**: Automatically generates step-by-step instructions or summaries using AI.
- 🌍 **Metadata Enrichment**: Captures location, category, and author info for every upload.
- 📁 **View Past Uploads**: Organized access to saved audio, transcripts, translations, and summaries.

---

## 📁 File Structure

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

## 🧑‍💻 How to Run Locally

1. **Clone the Repository**

```bash
git clone https://github.com/your-org/parampara-ai.git
cd parampara-ai
```

2. **Install Requirements**

```bash
pip install -r requirements.txt
```

3. **Set Up `.env`**

Create a `.env` file with your Google Gemini API Key:

```env
GEMINI_API_KEY=your_google_gemini_api_key
```

4. **Run the App**

```bash
streamlit run Home.py
```

---

## 📦 Requirements

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [google-generativeai](https://pypi.org/project/google-generativeai/)
- dotenv, Pillow, uuid, etc.

---

## 💡 Example Use Case

> Upload a 20-second audio clip of a village artisan describing pottery techniques in Telugu. Parampara AI will:
> - Transcribe the spoken content in Telugu.
> - Translate it to English.
> - Create a structured, step-by-step tutorial.

---

## 🙌 Credits

> 🛠️ This project was developed by **Team Dev_404** — **VISWAM.AI Interns** — during the **SoAI Program** organized by [**VISWAM.AI**](https://viswam.ai) & [**Swecha**](https://swecha.org).

---

## 📄 License

MIT License – feel free to use, modify, and share with attribution.

---