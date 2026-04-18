import streamlit as st
from PIL import Image
from google import generativeai as genai
from dotenv import load_dotenv
import os
from gtts import gTTS
import io

# -------------------- CONFIG --------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-3-flash-preview")

# -------------------- FUNCTIONS --------------------

def note_generation_english(images):
    prompt = """You are an expert visual analyst and structured note-taker.
Carefully examine the provided image(s), including all visible text, charts, diagrams, labels, symbols, and layout structure. 
Create a clear, well-organized, concise summary note based only on the visible content (no assumptions or external information). 
If something is unclear, briefly mention it.

Structure the response using Markdown with these exact section headings:
## Overview
## Key Information
## Visual Elements Breakdown
## Important Insights
## Unclear or Missing Information (only if needed)

Keep the tone neutral and analytical, avoid repetition.
Total response must not exceed 300 words."""

    response = model.generate_content([prompt] + images)
    return response.text


def note_generation_bangla(images):
    prompt = """You are an expert visual analyst and structured note-taker.
Carefully examine the provided image(s), including all visible text, charts, diagrams, labels, symbols, and layout structure. 
Create a clear, well-organized, concise summary note based only on the visible content (no assumptions or external information). 
If something is unclear, briefly mention it.

Structure the response using Markdown with these exact section headings:
## সারসংক্ষেপ
## মূল তথ্য
## ভিজ্যুয়াল উপাদান বিশ্লেষণ
## গুরুত্বপূর্ণ অন্তর্দৃষ্টি
## অস্পষ্ট বা অনুপস্থিত তথ্য (প্রয়োজন হলে)

Keep the tone neutral and analytical, avoid repetition.
Total response must not exceed 300 words."""

    response = model.generate_content([prompt] + images)
    return response.text


def audio_generation(text):
    speech = gTTS(text=text, lang='en', slow=False)
    audio_buffer = io.BytesIO()
    speech.write_to_fp(audio_buffer)
    return audio_buffer.getvalue()


def quiz_generation(images, difficulty, quiz_number):
    prompt = f"""You are an expert educator and quiz designer.
Based strictly on the provided content or image (no assumptions or external information), generate exactly {quiz_number} multiple-choice questions (MCQs) at the {difficulty} difficulty level.

Format the output using clean Markdown suitable for Streamlit.
Number each question clearly (e.g., **Question 1**, **Question 2**, etc.).

Each question must have exactly 4 options formatted with bullet points:
- A.
- B.
- C.
- D.

After all questions, add a separate section titled:
## ✅ Correct Answers

List the correct answers clearly (e.g., 1-A, 2-C, 3-B, etc.).

Keep the tone clear and appropriate for the {difficulty} level.
Do not invent missing information."""

    response = model.generate_content([prompt] + images)
    return response.text


# -------------------- UI --------------------

st.title("📚 Note Summary & Quiz Generator")
st.markdown("Upload your notes and get a summary along with quiz questions!")
st.divider()

with st.sidebar:
    st.header("Controls")

    images = st.file_uploader(
        "Upload your notes (jpeg, png, jpg)",
        type=["jpeg", "png", "jpg"],
        accept_multiple_files=True
    )

    pil_images = []
    if images:
        if len(images) > 5:
            st.error("Please upload a maximum of 5 images.")
        else:
            for img in images:
                pil_images.append(Image.open(img))

            st.subheader("Uploaded Notes:")
            cols = st.columns(len(images))
            for i, img in enumerate(images):
                with cols[i]:
                    st.image(img)

    selected_difficulty = st.selectbox(
        "Select Quiz Difficulty Level",
        ["Easy", "Medium", "Hard"],
        index = None
    )

    selected_quiz_number = st.selectbox(
        "Select Number of Questions",
        [20,30,40,50],
        index = None
    )

    select_language = st.selectbox(
        "Select Language for Summary",
        ["English", "Bangla"],
        index = None
    )

    press = st.button("Generate Summary & Quiz", type="primary")


# -------------------- MAIN LOGIC --------------------

if press:
    if not images:
        st.error("Please upload at least one image.")
    else:

        # -------- Summary --------
        with st.container(border=True):
            st.subheader("📝 Summary of Your Notes")
            with st.spinner("Generating summary..."):
                if select_language == "Bangla":
                    note_text = note_generation_bangla(pil_images)
                else:
                    note_text = note_generation_english(pil_images)

                st.markdown(note_text)

        # -------- Audio --------
        with st.container(border=True):
            st.subheader("🔊 Audio Version")
            cleaned_text = note_text.replace("#", "").replace("*", "")
            with st.spinner("Generating audio..."):
                audio = audio_generation(cleaned_text)
                st.audio(audio)

        # -------- Quiz --------
        with st.container(border=True):
            st.subheader(f"🧠 Quiz Questions ({selected_difficulty})")
            with st.spinner("Generating quiz questions..."):
                quiz = quiz_generation(
                    pil_images,
                    selected_difficulty,
                    selected_quiz_number
                )
                st.markdown(quiz)