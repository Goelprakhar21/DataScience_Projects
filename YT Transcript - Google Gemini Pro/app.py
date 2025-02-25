import streamlit as st #For front end integration of the webpage
from dotenv import load_dotenv
import os
import re

load_dotenv() #to load all the environment variables
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
prompt = "You are a Youtube Video Summariser, You'll be taking a transcript text and summarising the entire video and providing the important summary in points, within 200-500 words. Please provide the summary using the text which is provided here:  "

#to extract transcript from the video
def extract_transcript_details(youtube_video_url):
    try:
        query = re.search(r"v=([-\w]+)", youtube_video_url)
        if query:
            video_id = query.group(1)
            transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
            transcript = ""
            for i in transcript_text:
                transcript += " " + i['text']
            return transcript
        else:
            raise ValueError("Invalid YouTube URL")
    
    except Exception as e:
        raise e

#function to get summary based on the prompt from google gemini pro
def generate_gemini_content(transcript_text, prompt):

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt+ transcript_text)
    return response.text

st.title("YOUTUBE Transcript to Summarised text converter")
youtube_link=st.text_input('Enter your video link here:')

if youtube_link:
    video_id = youtube_link.split("v=")[-1].split("&")[0]
    st.image(f'https://img.youtube.com/vi/{video_id}/0.jpg', use_column_width=True)

if st.button("Get detailed summary"):
    transcript_text = extract_transcript_details(youtube_link)
    
    if transcript_text:
        summary = generate_gemini_content(transcript_text,prompt)
        st.markdown('Points created using the summary of the video:')
        st.write(summary)


        