📊 Project Report: Parampara AI
1.1. Team Information
Team Name: Dev_404

Team Members:

K V Jaya Harsha

MD Arif

Chandra

Mubeena Shaik

Jasmine

Date: July 23, 2025

1.2. Application Overview
Parampara AI is a multimodal preservation platform designed to archive India's oral and intangible cultural heritage. Built for use by artisans, elders, and cultural storytellers, it enables the collection of spoken stories, visual documentation (images/videos), and associated metadata into structured, accessible formats.

🔑 Updated MVP Capabilities:
Multi-File Upload Support: Users can now upload multiple files simultaneously—including audio, images, and videos—for each entry.

AI-Powered Processing via Gemini:

Transcription: Converts audio into original language text.

Translation: Automatically translates to English.

Structured Summarization: Extracts instructions or a high-level summary in JSON format.

Offline Corpus Storage: All data—including metadata, file URLs, transcription, translation, and summaries—is stored as .json files under the data/ directory, ensuring portability.

Enhanced Collection Viewer: Allows browsing all entries with previews for media, text fields, and summaries in a clean, sortable UI.

1.3. AI Integration (Gemini Multimodal API)
The application utilizes the Google Gemini 1.5 Flash model for a single-pass inference that outputs:

transcription_original_language

translation_english

summary_data in JSON format

✅ Prompt Highlights:
One structured prompt processes everything in one call.

Output formatting is enforced using markdown headers and JSON code block:

python-repl
Copy
Edit
**[Language] Transcription:**  
...
**English Translation:**  
...
**Summary JSON:**  
```json
{ ... }
🧩 Key Improvement:
The backend parser has been enhanced to gracefully handle malformed or non-JSON outputs by cleaning up responses and extracting valid JSON blocks reliably.

1.4. Technical Architecture & Enhancements
Component	Technology	Notes
Frontend UI	Streamlit	Simplified for rapid input and visual feedback
AI Backend	Gemini API (google-generativeai)	Single-call inference for transcription, translation, and summary
Storage	Local JSON corpus (/data/*.json)	Each entry is saved with file URLs and full metadata
Upload System	Streamlit file_uploader	Now supports multiple audio, image, and video files
File Metadata	Python uuid, os.path, mimetypes	Detects file types and saves structured URLs for all media types

1.5. New JSON Format Example (Post-Upload)
json
Copy
Edit
{
  "speaker_name": "Lakshmi",
  "location": "Srikakulam",
  "category": "Storytelling",
  "audio_urls": ["uploads/audio123.wav"],
  "image_urls": ["uploads/img1.jpg", "uploads/img2.jpg"],
  "video_urls": ["uploads/vid1.mp4"],
  "transcription_original_language": "నిన్న మా అమ్మమ్మ చెప్పిన కథ...",
  "translation_english": "Yesterday, my grandmother told a story about...",
  "summary_data": {
    "type": "story",
    "summary_text": "A story about resilience and wisdom shared by elders..."
  },
  "timestamp": "2025-07-27T12:45:00Z"
}
1.6. User Testing Updates (Week 2)
Based on feedback, the following enhancements were made:

Feedback	Fix Implemented
Lack of visual response during API call	st.spinner("Processing with Gemini...") added
JSON hard to understand	Now shown in expandable format, prettified
Difficult to find recent uploads	Collection page now sorts by latest timestamp first
Summary steps not clearly shown	Instructions now shown as numbered lists in the UI
Support for multiple uploads	Added multi-file upload UI for all file types (audio/image/video)

1.7. Roadmap Update (Post-Internship)
✅ Completed: Multi-file upload, advanced Gemini parsing, and file categorization

🔜 Planned:

Mobile support via Streamlit or Flutter WebView

Public-facing cultural story feed

Firebase-based cloud storage for profile-based corpus

NLP-based auto-categorization (e.g., recipe, myth, proverb)

1.8. Conclusion
This update takes Parampara AI closer to being a robust, field-ready tool for grassroots documentation efforts. By integrating multimodal upload, AI processing, and offline-first storage, the platform now offers a scalable way to preserve India’s diverse voices.