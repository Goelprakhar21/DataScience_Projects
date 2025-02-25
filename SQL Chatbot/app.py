from dotenv import load_dotenv
load_dotenv() #loading all the environment variables

import streamlit as st
import os
import sqlite3

import google.generativeai as genai


#configuring the API key stored in .env
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

#Creating a function to load google gemini model, providing query as response

def get_response_from_gemini(question,prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0],question])
    return response.text


#Creating another function to retrieve the queries from SQL Database

def fetch_sql_query(sql,db):
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    connection.commit()
    connection.close()
    for row in rows:
        print(row)
    return rows

#Defining the prompt for Gemini model
#Giving information to model that it needs to behave in a particular way


prompt = ["""
You are an expert in converting english questions to SQL Query based on the database details that are as follows.

The SQL Database has the name Countries and has the following columns - NAME, CAPITAL, CURRENCY and PHONECODE.
Each of these columns signifies some details like Name signifies country name. Capital signifies Country's Capital, Currency signifies the country's currency like India has INR, Britain has GBP and Phonecode signifies the dialing code for the country like India has +91, Pakistan has +92 etc.
\n For example
\n Example 1 - How many records are persent?, The sql command should return something like this, SELECT COUNT(*) FROM COUNTRIES;
\n Example 2 - Tell me all the countries using USD as it's currency?, The SQL Command should return something like this, SELECT * from COUNTRIES where CURRENCY="USD";

Also, The sql code should not have ''' in the beginning or end and sql word in the output.
The output commands should be directly executable in the SQL terminal.



"""
]


st.set_page_config(page_title = "App which can retirieve data from database based on your input")
st.header("App to retrieve SQL Data")

question = st.text_input('Input:',key='input')
submit = st.button("Submit your question")

#If submit is clicked
if submit:
    response=get_response_from_gemini(question,prompt)
    print(response)
    data = fetch_sql_query_sql_query(response,'Countries.db')
    st.subheader("The response is:")
    for row in data:
        print(row)
        st.header(row)
