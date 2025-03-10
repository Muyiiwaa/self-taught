import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from pdf import PDF
import time
import os
from dotenv import load_dotenv



# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# Set up Google Gemini-Pro AI model
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')


def generate_summary(transcript):
    prompt = f'''
    You are a very experienced educator. You are given a youtube video transcript and you need to create a 
    a detailed study note for the user. The note must only have the following segments:
    Lesson Title: [Title of the video]
    Learning Objectives: 
        [List of key concepts covered in the video that the learner should understand]
    Body:
        [An expert note of the video content. This should be detailed, informative 
        and should cover every key points of the video and additional input that will help the user.]
    Assessment:
        [A list of questions not more than ten to test the user's understanding of the video content.]
    
    You are given this youtube video transcript:{transcript}
    It is important to write extensively like a professional educator on the subject
     and you must never deviate from the video content. It is also important to not include asteriks in the titles and
     subheadings. Do not ever use any special character that is not part of FPDF standard font. I repeat do not use any
     special characters or puntuations that is going to cause Unicode Encoding exception.
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

def create_pdf(name, text):
    # Create a PDF object
    pdf = PDF('P', 'mm', 'Letter')
    # get total page numbers
    pdf.alias_nb_pages()
    # Set auto page break
    pdf.set_auto_page_break(auto = True, margin = 15)
    # Add a page and populate with text
    pdf.print_chapter(1, 'Summary', text=text)
    return pdf.output(name)

with st.sidebar:
    st.title('SELF-TAUGHT')
    st.divider()
    st.text_area('feedback', placeholder='Please leave your feedback here...',
                 label_visibility='hidden', height=170, max_chars=100)
    if st.button(label ='Submit', type='primary'):
        with st.spinner('Submitting feedback...'):
            time.sleep(1)
        st.success('Feedback submitted successfully!')
    st.divider()

st.title('SUMMARIZE WITH LEARNLIT')
st.divider()
with st.container(height=220):
    st.subheader('Your YouTube Video Study Companion!', divider=True)
    st.write('This tool is designed to help you get more value from your learning experience on youtube. Simply paste the URL of the video you are watching and we will provide you with a summary of the video, a list of key concepts, and a quiz to test your understanding of the material.')
url = st.text_input(label='url',
                    label_visibility='hidden', placeholder='https://www.youtube.com/watch?v=...')
url_button = st.button('Fetch Video Transcript', type='primary')
if url and url_button:
    transcript = extract_transcript_details(url)
    with st.spinner('Transcript fetched, now generating summary...'):
        summary = generate_summary(transcript)
    st.success('Summary generated successfully!')
    st.write(summary)
    download_pdf, clear_button = st.columns(2)
    with download_pdf:
        create_pdf(name='summary.pdf', text=summary)
        with open('summary.pdf', 'rb') as file:
            file_pdf = file.read()
        st.download_button(label="Download PDF",
                           data=file_pdf,
                           file_name="note.pdf",
                           mime='application/octet-stream')
    with clear_button:
        if st.button('Clear Output', type='secondary'):
            pass