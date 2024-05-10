import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

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

st.title('SELF-TAUGHT: AI-UPSKILLING COMPANION')
st.divider()
with st.container(height=220):
    st.subheader('Welcome to the AI-Upskilling Companion!', divider=True)
    st.write('Welcome to the AI-Upskilling Companion! This tool is designed to help you get more value from your learning experience on youtube. Simply paste the URL of the video you are watching and we will provide you with a summary of the video, a list of key concepts, and a quiz to test your understanding of the material.')
url = st.text_input(label='url',
                    label_visibility='hidden', placeholder='https://www.youtube.com/watch?v=...')
url_button = st.button('Fetch Video Transcript', type='primary')
if url and url_button:
    st.spinner('Fetching video transcript...')
    transcript = extract_transcript_details(url)
    st.write(transcript)
    
    