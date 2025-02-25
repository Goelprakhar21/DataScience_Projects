import streamlit as st
import pandas as pd
import re
import emoji
from collections import Counter
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Function to parse chat data (assuming the provided logic is functional)
def parse_chat_data(chat_file):
    parsed_data = []
    try:
        with open(chat_file, encoding="utf-8") as fp:
            # Implement parsing logic here (replace with your actual parsing code)
            pass
        df = pd.DataFrame(parsed_data, columns=['Date', 'Time', 'Author', 'Message'])
        return df
    except Exception as e:
        st.error(f"Error parsing chat data: {e}")
        return None  # Return None to indicate parsing failure

# Sentiment analysis function
def get_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    return sentiment['compound']

# Streamlit app
st.title("Enhanced WhatsApp Chat Analyzer")
st.subheader("Analyze your WhatsApp chat conversations!")

# Upload chat file
uploaded_file = st.file_uploader("Upload your WhatsApp chat file (.txt)", type="txt")

if uploaded_file is not None:
    # Parse chat data
    df = parse_chat_data(uploaded_file.name)

    if df is not None:  # Check if parsing was successful
        st.success("Chat data parsed successfully!")

        # Add sentiment score column
        df['Sentiment'] = df['Message'].apply(get_sentiment)

        # Display basic information
        st.subheader("Basic Information")
        st.write(f"Total Messages: {df.shape[0]}")
        st.write(f"Unique Authors: {df['Author'].nunique()}")

        # Analysis by author
        st.subheader("Analysis by Author")
        author_options = df['Author'].unique()
        selected_author = st.selectbox("Select Author", author_options)
        author_df = df[df['Author'] == selected_author]

        # Author sentiment distribution
        st.write(f"Author Sentiment Distribution for {selected_author}")
        fig = px.histogram(author_df, x='Sentiment', nbins=10)
        st.plotly_chart(fig)

        # Author word cloud
        st.write(f"Word Cloud for {selected_author}")
        text = ' '.join(author_df['Message'])
        stopwords = set(STOPWORDS)
        stopwords.update(['whatsapp', 'group', 'https', 'www'])  # Add custom stopwords

        wordcloud = WordCloud(width=800, height=600, stopwords=stopwords).generate(text)
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot()

        # Activity heatmap (placeholder)
        st.write("Activity Heatmap (requires datetime parsing)")
        # Uncomment and implement the following code for activity heatmap
        # df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])  # Assuming 'Date' and 'Time' are in appropriate format
        # df['Hour'] = df['Datetime'].dt.hour
        # df['Day'] = df['Datetime'].dt.weekday

        # activity_df = df.groupby(['Hour', 'Day']).size().unstack(fill_value=0)
        # fig = px.heatmap(activity_df, color_continuous_scale='viridis')  # Adjust color scale as needed
        # st.plotly_chart(fig)

    else:
        st.error("Chat data parsing failed.")

st.stop()
