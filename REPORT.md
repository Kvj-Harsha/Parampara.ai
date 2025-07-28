# Project Report: Parampara AI

## 1.1. Team Information

* **Team Name:** Dev_404
* **Team Members:**
    * K V Jaya Harsha
    * MD Arif
    * Chandra
    * Mubeena Shaik
    * Jasmine
* **Date:** July 23, 2025

## 1.2. Application Overview

**Parampara AI** is an intelligent platform engineered to bridge the gap between India's rich oral traditions and modern digital preservation. It empowers local artisans, storytellers, and knowledge keepers from every corner of India to document, preserve, and share their invaluable cultural heritage.

The Minimum Viable Product (MVP) focuses on the following core functionalities:

1.  **Audio Ingestion:** Users can upload audio recordings in various Indic languages.
2.  **AI-Powered Processing:** A single, efficient call to the Google Gemini API performs three tasks:
    * **Transcription:** Converts the spoken audio into text in its original language.
    * **Translation:** Translates the transcription into English.
    * **Structured Summarization:** Generates a concise, structured JSON summary of the content, identifying key themes, instructions, or narratives.
3.  **Offline-First Data Corpus:** All processed data, including metadata and the AI-generated content, is saved as a structured JSON file in a local `data/` directory. This approach ensures that a corpus of knowledge is built locally, accessible even without an internet connection, and can be easily backed up or migrated.
4.  **Data Viewer:** A built-in interface allows users to browse and review all the collected data entries.

The platform is built with Streamlit and deployed on Hugging Face Spaces for universal accessibility.

## 1.3. AI Integration Details

The intelligence of **Parampara AI** is driven by Google's `gemini-1.5-flash` model. This model was strategically chosen for its optimal blend of advanced multimodal capabilities, speed, and cost-effectiveness, making it ideal for our MVP.

Our AI integration strategy is centered on **efficient, multi-task prompt engineering**. Instead of making separate API calls for transcription, translation, and summarization, we engineered a single, comprehensive prompt that instructs the model to perform all three actions sequentially within one request.

**The Prompting Strategy:**

1.  **Input:** The model receives two inputs: the user's audio file and a detailed text prompt.
2.  **Instructions:** The prompt explicitly asks the model to:
    * First, transcribe the audio in the user-specified Indic language.
    * Second, translate the resulting transcription into fluent English.
    * Third, analyze the English text and generate a summary in a specific JSON format. The format is conditional: if the content is a tutorial, it should produce a list of `instructions`; otherwise, it should produce a `summary_text`.
3.  **Output Formatting:** The prompt commands the model to structure its entire response with clear markdown headers (`**[Language] Transcription:**`, `**English Translation:**`, `**Summary JSON:**`) and a JSON code block. This predictable structure is crucial for reliable parsing on the backend.

This single-call approach significantly reduces latency and API costs, making the tool more responsive and scalable.

## 1.4. Technical Architecture & Development

The architecture is designed for rapid development, simplicity, and accessibility, aligning with the MVP goals.

* **Frontend Framework:** **Streamlit** was chosen for its ability to quickly create interactive, data-centric web applications with pure Python.
* **AI Model & API:** **Google Gemini 1.5 Flash** is accessed via the `google-generativeai` Python SDK.
* **Deployment Platform:** **Hugging Face Spaces** provides a free, scalable, and easy-to-manage environment for deploying Streamlit applications. It integrates seamlessly with our Git-based workflow.
* **Data Storage (Offline-First):** The application uses the server's local file system as its database. Each processed entry is saved as a unique `.json` file in the `/data` directory. This design choice makes the collected corpus portable, resilient, and independent of external database services for the MVP stage.
* **Key Python Libraries:**
    * `streamlit`: For the web interface.
    * `google-generativeai`: For interacting with the Gemini API.
    * `python-dotenv`: To manage the API key securely.
    * `pathlib`, `glob`: For file system operations and data retrieval.

## 1.5. User Testing & Feedback

### Methodology (Week 2)

During the second week, we conducted a beta testing cycle with a small, targeted group to gather initial feedback on the MVP.

* **Recruitment:** We recruited 5 testers from our immediate network, comprising university students with an interest in linguistics and local culture. This group was chosen to reflect our early adopter persona.
* **Task:** Testers were given the link to the deployed Hugging Face Space and a single, clear task:
    > "Please record a 30-second audio clip of yourself telling a short story or explaining a simple recipe in your native language. Use the 'Transcribe & Translate Audio' feature to process it. Then, go to the 'View Your Data Collection' page to find and review your entry. Report back on your experience."
* **Feedback Collection:** Feedback was collected via a shared Google Doc where users could log issues, suggestions, and general comments. We specifically asked them to note any slowness or unresponsiveness to simulate a low-bandwidth user experience.

### Insights & Iterations

The feedback was invaluable for refining the user experience. The following table summarizes the key insights and the changes we implemented.

| Feedback Received                                                                                    | Our Analysis                                                                                             | Iteration / Change Implemented                                                                                                                               |
| ---------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| "It was unclear if the app was working after I clicked the 'Process' button. I clicked it twice."      | The lack of immediate visual feedback on a long-running task caused user confusion.                      | Implemented `st.spinner()` to show a loading message ("Processing audio with Gemini AI...") during the API call.                                              |
| "The raw JSON response was hard to read and not very useful for me."                                   | The initial design showed the raw API response prominently, which was only useful for debugging.         | The raw response was moved into a collapsed `st.expander` titled "Raw Gemini API Response (for debugging)".                                                      |
| "I couldn't easily find my latest submission on the collection page."                                  | The file list was not sorted, making it difficult to find the most recent entries.                       | Modified the `glob` function to sort JSON files by modification time (`os.path.getmtime`), displaying the newest entries first.                               |
| "The summary section was just a block of text. It would be better if the steps were listed clearly." | The app was not parsing the `instructions` array from the summary JSON and displaying it as a formatted list. | Enhanced the UI to parse and display the `instructions` array as a clean, numbered list. This directly addresses user feedback by making tutorial-style content significantly easier to read and follow. |

## 1.6. Project Lifecycle & Roadmap

### A. Week 1: Rapid Development Sprint

* **Plan:**
    * **Day 1-2:** Set up the project structure, initialize the Git repository, and build the basic multi-page Streamlit app with placeholder pages for `Upload` and `Collection`.
    * **Day 3-4:** Integrate the Gemini API. Focus on the core `generate_content` call with both audio and text inputs. Engineer the initial multi-task prompt.
    * **Day 5-6:** Develop the backend logic for saving processed data to JSON files. Implement the response parsing logic to reliably extract transcription, translation, and summary.
    * **Day 7:** Refine the UI, add user instructions, and deploy the initial version to streamlit cloud.
* **Execution:** The plan was executed successfully. By the end of Week 1, we had a functional, deployed MVP that met all core requirements, including the offline-first data saving mechanism.

### B. Week 2: Beta Testing & Iteration Cycle

This week was dedicated to refining the MVP based on real user feedback. The methodology, insights, and iterations are detailed in section **1.5. User Testing & Feedback**. The primary outcome was a more stable, user-friendly, and intuitive application.

### C. Weeks 3-4: User Acquisition & Corpus Growth Campaign

This phase focused on moving from a functional prototype to a tool with real-world usage and data contributions from across India.

* **Target Audience & Channels:**
    * **Primary Audience:** University students in humanities departments (Linguistics, Anthropology, Cultural Studies) from various universities across India.
    * **Secondary Audience:** Members of local literary clubs, online storytelling communities, and cultural organizations spread across different Indian states.
    * **Justification:** This diverse, pan-India audience is highly motivated by cultural preservation, possesses a wide range of linguistic knowledge, and is well-positioned to provide high-quality, regionally diverse audio contributions.
    * **Channels:** Direct email outreach to university professors nationwide, posts in pan-India student and community forums (e.g., on platforms like Reddit, Facebook, Telegram), and collaborations with cultural influencers.
* **Growth Strategy & Messaging:**
    * **Key Message:** "Your Voice, Our Heritage. In 30 seconds, you can preserve a piece of your culture forever. Use Parampara AI to help archive India's oral traditions."
    * **Promotional Materials:** We created simple text-based posts for WhatsApp and a more visual post for social media.
        * **Example WhatsApp Message:**
            > "Hello! We are Dev_404, a team building Parampara AI, a free tool to help preserve our local languages and stories. If you have 30 seconds, please visit our app, record a short story or proverb in your mother tongue, and help us grow this valuable digital archive for future generations. Link: \[Website Link\]"
* **Execution & Results (Projected):**
    * **Actions:** Sent emails to department heads at various universities, posted in 20+ national student and community groups, and made daily posts on social media.
    * **Metrics (Projected Results):**
        * **Unique Users:** We project acquiring **180 unique users** over the two-week campaign.
        * **Corpus Units:** We project the collection of **350 individual data contributions** (JSON files), forming a substantial initial corpus.
        * **User Feedback:** We anticipate receiving feedback highlighting a desire for a mobile-native app for easier recording and requests for more languages to be officially supported in the UI.

### D. Post-Internship Vision & Sustainability Plan

Our experience during the internship has validated the need for this platform and informed our vision for its future.

* **Major Future Features:**
    1.  **Scalable Cloud Architecture & User Profiles:** Transition from the MVP's local storage to a robust cloud database (e.g., Firebase Firestore). This foundational upgrade will enable user profiles, secure data management, and a collaborative, real-time environment for community contributions.
    2.  **Community Feed:** Create a public feed where users can browse, listen to, and engage with public contributions, fostering a sense of community.
    3.  **Batch Upload & Processing:** Implement a feature for researchers and institutions to upload and process entire archives of audio data at once.
* **Community Building:**
    * Establish a Discord server or Telegram channel for power users, linguists, and cultural enthusiasts to discuss the project, suggest features, and help moderate content.
    * Launch a "Story of the Week" initiative to feature the best contributions on social media.
* **Scaling Data Collection:**
    * Form official partnerships with universities, cultural NGOs (e.g., INTACH), and government bodies across India to integrate Parampara AI into their archival workflows.
    * Organize on-ground "documentation drives" in various rural areas to collect stories from elders who may not have access to smartphones.
* **Sustainability:**
    * **Grants & Funding:** Actively apply for grants from cultural preservation foundations (e.g., UNESCO, Ford Foundation) and technology-for-good programs.
    * **Freemium Model:** Keep the core features free for individual contributors while offering premium, paid features for institutions, such as advanced data analytics, private collection management, and dedicated support.
