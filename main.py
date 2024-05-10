import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import time
import os
from dotenv import load_dotenv



# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# Set up Google Gemini-Pro AI model
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')


def generate_summary(transcript):
    prompt =f'''
    You are a youtube video transcript summarizer. You are given a youtube video transcript and you need to summarize the video in the format below.
    Lesson Title: [Title of the video]
    Learning Objectives: 
        [List of key concepts covered in the video that the learner should understand]
    Summary:
        [An expert summary of the video content. This should be detailed, informative and should cover the key points of the video.]
    Additional Resources:
        [Suggest additional resources or references related to the video content that you think the user should should checkout.]
    Assessment:
        [Create a set of questions not more than 5 to test the user's understanding of the video content.]
    
    You are given the following youtube video transcript:{transcript}
    There should not be more than 12 words on a single line in the summary section and summary section should
    contain at least 100 words.
    This is extremely important as it will help parse the output into a pdf converter.
    Let me repeat again, there should not be more than 12 words on a single line in the summary section.
    '''
    summary = model.generate_content(prompt)
    return summary.text

# extract video id from url and fetch transcript
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split('v=')[1].split('&')[0]  # Improved extraction
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript
    except Exception as e:
        st.error(f"Failed to fetch transcript: {e}")
        return None

# convert transcript text to pdf
def create_pdf_from_string(pdf_filename, text):
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    lines = text.split("\n")
    y = 750
    for line in lines:
        c.drawString(50, y, line)
        y -= 14
    c.save()

st.title('SELF-TAUGHT: AI-UPSKILLING COMPANION')
st.divider()
with st.container(height=220):
    st.subheader('Welcome to the AI-Upskilling Companion!', divider=True)
    st.write('Welcome to the AI-Upskilling Companion! This tool is designed to help you get more value from your learning experience on youtube. Simply paste the URL of the video you are watching and we will provide you with a summary of the video, a list of key concepts, and a quiz to test your understanding of the material.')
url = st.text_input(label='url',
                    label_visibility='hidden', placeholder='https://www.youtube.com/watch?v=...')
url_button = st.button('Fetch Video Transcript', type='primary')
if url and url_button:
    transcript = extract_transcript_details(url)
    summary = generate_summary(transcript)
    with st.spinner('Fetching video transcript and generating summary...'):
        time.sleep(2)
    st.write(summary)
    st.button('Download Transcript PDF', type='secondary', on_click=create_pdf_from_string, args=('lesson_plan2.pdf', summary))
    
    