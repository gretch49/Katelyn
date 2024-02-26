# Run the code using: streamlit run app_SL.py

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
katelyn_questions_planned = [
    "Okay, great. Let me ask you some questions to better plan an itinerary for you. \n\n"
    "First, where are you going? You can be specific, like “New York City,” or more general, like “Eastern Europe.” "
    "If it's helpful, you can also give me a list of places.",
    'I’ve always wanted to go there! When do you plan on going? If you’re not sure, you can say “unsure.” ',
    'How long do you plan to travel for? You can say something general like “a few days,” or be more specific and say ' \
    'something like “2 weeks.” If you’re not sure, you can say “unsure.” ',
    'Who do you plan on going with? I’d like to know their ages and names, or their relationships to you.' \
        ' If it’s a solo trip, you can say “myself.” ',
    "Let's talk about the fun stuff! What do you (and your companions) like to do on vacation? Maybe you "
        ' just want to lounge on the beach and suntan, but I bet you want to do some activities too. Tell me '
        'some activities you enjoy, like biking, sight-seeing, eating local cuisine, shopping, or meeting new people. ',
    'Now let’s talk logistics. What’s your estimated budget for this trip? I’ll assume USD unless you specify otherwise. ',
    'Do you have any other considerations for me to keep in mind? For example, you could tell me you don’t want to go hiking, '
        'or that you’re traveling with someone with specific needs. Otherwise, you can just say "no." ',
    'Let me know if there are things you specifically want recommendations on, like where to rent a car, what the best budget '
        'hotel is, or how to use public transit. ',
    "And have you thought about how you'll be getting around? Let me know if you plan on using your own car, renting a car, "
        "using public transit, or a mixture of transportation. ",
    "Last question! So I can better plan for your budget, where are you traveling from? In other words, where's home for you? \n\n"
        "Once you answer, please give me a moment while I research an itinerary for you."
    ]
katelyn_questions_unplanned = [
    "I understand, it’s a big world out there! Let me help you narrow down some ideas. Do you prefer warm weather or "
        "cool weather? ",
    'When do you plan on going? If you’re not sure, you can say “unsure.”',
    'How long do you plan to travel for? You can say something general like “a few days,” or be more specific and say '
        'something like “2 weeks.” If you’re not sure, you can say “unsure.” ',
    'Who do you plan on going with? I’d like to know their ages and names, or their relationships to you.' 
        ' If it’s a solo trip, you can say “myself.” ',
    "Let's talk about the fun stuff! What do you (and your companions) like to do on vacation? Maybe you "
        ' just want to lounge on the beach and suntan, but I bet you want to do some activities too. Tell me '
        'some activities you enjoy, like biking, sight-seeing, eating local cuisine, shopping, or meeting new people. ',
    'Do you have any restrictions on going out of the US? ',
    "Is there any region you’ve always wanted to visit, or anything on your bucket list? "
        "It's okay if you don't have anything in mind.",
    'Do you have any other considerations for me to keep in mind? For example, you could tell me you don’t want to go '
        'hiking, or that you’re traveling with someone with specific needs. Otherwise, you can just say "no." ',
    'Now let’s talk logistics. What’s your estimated budget for this trip? I’ll assume USD unless you specify otherwise. ',
    "Last question! So I can better plan for your budget, where are you traveling from? In other words, where's home for you? \n\n"
        "Once you answer, please give me a moment while I research an itinerary for you."
]

### FUNCTIONS ###

def katelyn_chatbot():
    st.set_page_config(layout="wide")
    st.title("ARCHIVE: Katelyn, your Travel Assistant Chatbot")
    st.caption("This chatbot is out-of-date. See the updated version at: https://katelyn-update.streamlit.app/")

    #########################
    # If the code has never been run before, say you're Katelyn
    # Initialize session state variables

    # This means if st.session_state is empty (beginning of the session with the chatbot), i is set to 0...
    # As Streamlit runs the code every time a user does something, we don't want to set i = 0...
    # because that will make i = 0 every time the user does anything
    if "i" not in st.session_state:
        st.session_state.i = 0
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content":"Hi, I'm Katelyn, your virtual travel assistant. "
                                    "I’m excited to help you plan your trip! \n\n To get started, I’d like to know how much of your trip "
                                    "you have planned. Do you know where you're going, or is the world your oyster?"}]
    if "response" not in st.session_state:
        st.session_state.all_responses = []
    if "chat_finished" not in st.session_state:
        st.session_state.chat_finished = False
    if "prompt" not in st.session_state:
        st.session_state.prompt = ""
    if "gpt_planned" not in st.session_state:
        st.session_state.gpt_planned = 0

    #Let's double check we're still going...
    if not st.session_state.chat_finished:

        ### This part is writing the conversation every time Streamlit runs the code 
        ### (every time a user does something)
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
        #########################
            
    if new_response := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": new_response})
        st.chat_message("user").write(new_response)

        ### If this is the first time the user has said something, send that message in a prompt to GPT to see how planned the user is
        if len(st.session_state.messages) == 2:
            prompt_for_route = f"The prompt is answering the question: 'Do you know where you're going?' If it sounds like the user knows where they're going, return 1. If the user sounds unsure or says no, return 2. Return a number only. The prompt is: {new_response}"
            gpt_response = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[{"role": "system", "content": prompt_for_route}],
            max_tokens=1
            )
            st.session_state.gpt_planned = int(gpt_response.choices[0].message.content)
        
        ### Go this route if the user has planned a location
        if st.session_state.gpt_planned == 1 and st.session_state.i < len(katelyn_questions_planned):
            time.sleep(.5)
            st.session_state.messages.append({"role": "assistant", "content": katelyn_questions_planned[st.session_state["i"]]})
            st.chat_message("assistant").write(katelyn_questions_planned[st.session_state["i"]])
            st.session_state.i += 1

        ### Go this route if the user hasn't planned a location
        elif st.session_state.gpt_planned == 2 and st.session_state.i < len(katelyn_questions_unplanned):
            time.sleep(.5)
            st.session_state.messages.append({"role": "assistant", "content": katelyn_questions_unplanned[st.session_state["i"]]})
            st.chat_message("assistant").write(katelyn_questions_unplanned[st.session_state["i"]])
            st.session_state.i += 1

        else:
            print(1)
            st.session_state.chat_finished = True
            st.experimental_rerun()

    st.session_state.all_responses = st.session_state.messages
    return st.session_state.all_responses

### END OF FUNCTION ###

def display_itinerary(messages):
    st.title("Katelyn, your Travel Assistant Chatbot")
    st.caption("I'll create a personalized travel itinerary in minutes.")
    
    messages.append({"role": "system", "content": "You are a virtual travel agent. Your job is to create a personalized itinerary based on this conversation. Keep the itinerary to less than 3000 characters."})

    gpt_response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=messages,
        max_tokens=3000
        )
    itinerary = gpt_response.choices[0].message.content

    st.write(itinerary)


########################################################################################################



if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title("ARCHIVE: Katelyn, your Travel Assistant Chatbot")
    st.caption("This chatbot is out-of-date. See the updated version at: https://katelyn-update.streamlit.app/")

    #if not "chat_finished" in st.session_state:  # Initialize if not present
        #st.session_state.chat_finished = False

    #if not st.session_state.chat_finished:
        #st.session_state.prompt = katelyn_chatbot()  # Call chatbot function if chat is not finished
        
    
    #else:
        #display_itinerary(st.session_state.prompt)  # Display itinerary if chat is finished
