# Note Summary & Quiz Generator

**An intelligent web app that turns your lecture slides, notes, or study images into a clean summary + personalized quiz in seconds.**

Built as a **Streamlit** application with AI-powered image understanding, summarization, and quiz generation.

![App Interface](https://note-quiz-app-mini.streamlit.app/)  

## ✨ Features

- **Smart Note Upload**  
  Supports JPEG, PNG, and JPG files (up to 200 MB per file). Perfect for lecture slides, whiteboard photos, textbook pages, etc.

- **AI-Powered Summary**  
  Automatically extracts and organizes content into:
  - **Overview**
  - **Key Information** (with bullet points)
  - **Visual Elements Breakdown** (diagram analysis, labels, branding)
  - **Important Insights**

- **Customizable Quiz**  
  - Choose difficulty level (Easy / Medium / Hard)
  - Select number of questions (1–20)
  - Generates high-quality multiple-choice questions based on the uploaded notes

- **Audio Support**  
  Built-in audio player with transcription (TTS of the summary or extracted audio notes)

- **Instant Feedback**  
  Shows correct answers at the bottom for self-assessment

- **Modern Dark UI**  
  Clean, student-friendly interface with one-click generation

## 📸 Screenshots

<img width="1919" height="941" alt="Screenshot 2026-04-18 004356" src="https://github.com/user-attachments/assets/92b55d47-ef70-4561-b7b4-c6eb1bcffcc4" />


## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Streamlit
- Required API keys (OpenAI / Grok / Anthropic – depending on your backend)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/note-summary-quiz-generator.git
cd note-summary-quiz-generator

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file and add your API keys
cp .env.example .env
# Edit .env with your keys (GROK_API_KEY or OPENAI_API_KEY)
