import streamlit as st
import pandas as pd
import numpy as np
import emoji
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import regex
import plotly.express as px
import io

@st.cache
def load_data(file):
    def get_datapoint(line):
        split_line = line.split(' - ')
        date_time = split_line[0]
        date, time = date_time.split(', ')
        message = " ".join(split_line[1:])
        if ": " in message:
            author = message.split(": ")[0]
            message = ": ".join(message.split(": ")[1:])
        else:
            author = None
        return date, time, author, message

    data = []
    with io.StringIO(file.getvalue().decode("utf-8")) as fp:
        message_buffer = []
        date, time, author = None, None, None
        while True:
            line = fp.readline()
            if not line:
                if len(message_buffer) > 0:
                    data.append([date, time, author, ' '.join(message_buffer)])
                break
            line = line.strip()
            if regex.match(r'^([0-9]{1,2})/([0-9]{1,2})/([0-9]{2,4}), ([0-9]{1,2}):([0-9]{2}) ([APMapm]{2}) -', line):
                if len(message_buffer) > 0:
                    data.append([date, time, author, ' '.join(message_buffer)])
                message_buffer.clear()
                date, time, author, message = get_datapoint(line)
                message_buffer.append(message)
            else:
                message_buffer.append(line)

    df = pd.DataFrame(data, columns=["Date", 'Time', 'Author', 'Message'])
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def split_count(text):
    emoji_list = []
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.EMOJI_DATA for char in word):
            emoji_list.append(word)
    return emoji_list

def display_cloud(df):
    text = " ".join(message for message in df.Message if message)
    stopwords = set(STOPWORDS)
    stopwords.update(df.Author.dropna().unique())  # Remove author names from word cloud
    wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(plt)

def display_stats(df):
    total_messages = df.shape[0]
    media_messages = df[df["Message"] == '<Media omitted>'].shape[0]
    emojis = sum(df['emoji'].str.len())
    links = np.sum(df.urlcount)

    st.write("Total messages in this conversation: ", total_messages)
    st.write("Total number of media messages: ", media_messages)
    st.write("Number of emojis in a conversation: ", emojis)
    st.write("Number of links shared: ", links)

    for author in df.Author.unique():
        req_df = df[df["Author"] == author]
        if req_df.shape[0] > 0:
            words_per_message = (np.sum(req_df['Word_Count'])) / req_df.shape[0]
        else:
            words_per_message = 0
        media = df[(df["Message"] == '<Media omitted>') & (df["Author"] == author)].shape[0]
        emojis = sum(req_df['emoji'].str.len())
        links = sum(req_df["urlcount"])

        st.write(f"Stats of {author} -")
        st.write("Messages Sent: ", req_df.shape[0])
        st.write("Average Words per message: ", words_per_message)
        st.write("Media Messages Sent: ", media)
        st.write("Emojis Sent: ", emojis)
        st.write("Links Sent: ", links)

def display_chart(df):
    emoji_df = pd.DataFrame(Counter([a for b in df.emoji for a in b]).items(), columns=['emoji', 'count'])
    fig = px.pie(emoji_df, values='count', names='emoji')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig)

st.title("Chat Analysis")
uploaded_file = st.file_uploader("Upload a chat file", type=["txt"])
if uploaded_file:
    try:
        df = load_data(uploaded_file)
        df['emoji'] = df["Message"].apply(split_count)
        df['urlcount'] = df.Message.apply(lambda x: len(regex.findall(r'(https?://\S+)', x)))
        df['Letter_Count'] = df['Message'].apply(lambda s: len(s) if s else 0)
        df['Word_Count'] = df['Message'].apply(lambda s: len(s.split(' ')) if s else 0)
        df["MessageCount"] = 1

        st.write("Word Cloud:")
        display_cloud(df)

        st.write("Stats:")
        display_stats(df)

        st.write("Pie Chart:")
        display_chart(df)
    except Exception as e:
        st.error(f"An error occurred: {e}")
