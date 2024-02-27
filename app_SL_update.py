#!/usr/bin/env python3
# Run the code using: streamlit run app_SL_update.py

import streamlit as st
import os
from dotenv import load_dotenv
import openai
import time

# Load the environment variables
load_dotenv()
# Fetch the API key from the environment variable
gretchens_api_key = os.getenv("OPEN_API_KEY")
client = openai.OpenAI(api_key=gretchens_api_key)

st.title("Katelyn 2.0, your Travel Agent Chatbot")
st.caption("I'll create a personalized travel itinerary in minutes.")
setup = "You are a virtual travel agent named Katelyn. You need to get answers from the user about their upcoming trip in order to make a day-by-day itinerary for them. Keep a natural conversation but make sure you ask them about their destination, who they're going with, what activities they and their companions want to do, what season, what duration, what budget, where they're traveling from, if they need transportation advice, if they need any other advice, if they have any considerations like someone who is physically disabled, and any other necessary details. Print out a day-by-day itinerary when you have all the info you need."

if "messages" not in st.session_state:
    # Initialize `messages` as a list and include both the system and the first assistant message
    st.session_state.messages = [
        {"role": "system", "content": setup},
        {"role": "assistant", "content": "Hi, I'm Katelyn. I’m excited to help you plan your trip! \n\nTo get started, I’d like to know how much of your trip you have planned. Do you know where you're going, or is the world your oyster?"}
    ]

for message in st.session_state.messages:
    if message['role'] == 'user':
        # Display user message
        st.chat_message("user").write(message['content'])
    elif message['role'] == 'assistant':
        # Display AI-generated message
        st.chat_message("assistant").write(message['content'])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)


    gpt_response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=st.session_state.messages,
        max_tokens=3000
        )

    
    msg = gpt_response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
