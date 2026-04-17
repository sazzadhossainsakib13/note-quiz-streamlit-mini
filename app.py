import streamlit as st
from PIL import Image
from google import genai
from dotenv import load_dotenv
import os
from PIL import Image
from gtts import gTTS
import io

#API Working
#loading environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

#innitializing the Gemini API client
client = genai.Client(api_key=api_key)



#note genaration function

def note_generation_english(image):
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
        
        Keep the tone neutral and analytical, avoid repetition, use concise language. 
        Total response must not exceed 300 words."""
    Response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[image,prompt],
        )
    return Response.text
def audio_generation(text):
    
    speech =  gTTS(text=text, lang='en', slow=False)
    audio_buffer = io.BytesIO()
    speech.write_to_fp(audio_buffer)
    return audio_buffer.getvalue()
def quiz_generation(image,difficulty,quiz_number):
    prompt = f"""You are an expert educator and quiz designer. 
        Based strictly on the provided content or image (no assumptions or external information), generate exactly {quiz_number} multiple-choice questions (MCQs) at the {difficulty} difficulty level.
        
        Format the output using clean Markdown suitable for Streamlit (st.markdown). 
        Number each question clearly (e.g., **Question 1**, **Question 2**, etc.).
        Each question must have exactly 4 options formatted with bullet points:
        - A. 
        - B. 
        - C. 
        - D. 
        
        After all questions, add a separate section titled:
        ## ✅ Correct Answers
        and list the correct answers clearly (e.g., 1-A, 2-C, 3-B, etc.).
        
        Keep the tone clear and appropriate for the {difficulty} level, avoid repetition, do not invent missing information, and ensure the structure is clean and readable for direct Markdown rendering."""
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[image,prompt],
    )
    return response.text



#title section
st.title("Note Summary & Quiz Generator")
st.markdown("Upload your notes and get a summary along with quiz questions to test your understanding!")
st.divider()


#sidebar
with st.sidebar:
    st.header("controls")
    #working with image
    images = st.file_uploader(
        "Upload your notes ('jpeg', 'png','jpg')",
        type=["jpeg", "png", "jpg"],
        accept_multiple_files=True
        )
    
    pil_images = []
    for img in images:
        pil_images.append(Image.open(img))
    if images:
        if len(images) > 5:
            st.error("Please upload a maximum of 5 images.")
        else:
            st.subheader("Uploaded Notes:")
            col = st.columns(len(images))
            for i,img in enumerate(images):
                with col[i]:
                    st.image(img)

    #difficulty level
    selected_difficulty = st.selectbox(
        "Select Quiz Difficulty Level",
        options=["Easy", "Medium", "Hard"],
        index=None
    )
    st.header("Number of Questions in Quiz")
    selected_quiz_number = st.selectbox(
        "Select Number of Questions",
        options=[5,10,15,20,25,30],
        index=None
    )

    #button to generate quiz
    press = st.button("Generate Summary & Quiz",type="primary")


if press:
    if not images:
        st.error("Please upload at least one image of your notes.")
    elif not selected_difficulty:
        st.error("Please select a difficulty level for the quiz.")
    elif images and selected_difficulty:
        #note
        with st.container(border=True):
            st.subheader("Summary of Your Notes:")
            #the summary will be generated here by API call and displayed in the text area below
            with st.spinner("Generating summary..."):
                note_text = note_generation_english(pil_images)
                st.markdown(note_text)
        #audioprocessing
        with st.container(border=True):
            note_text = note_text.replace("#", "")
            note_text = note_text.replace(",", "")
            note_text = note_text.replace("'", "")
            note_text = note_text.replace("-", "")
            note_text = note_text.replace("(", "")
            note_text = note_text.replace(")", "")
            st.subheader("Audio Transcription:")
            with st.spinner("Generating audio..."):
                audio = audio_generation(note_text)
                st.audio(audio)
        #quiz
        with st.container(border=True):
            st.subheader(f"Quiz Questions ({selected_difficulty}):")
            with st.spinner("Generating quiz questions..."):
                quiz = quiz_generation(pil_images,selected_difficulty,selected_quiz_number)
                st.markdown(quiz)
