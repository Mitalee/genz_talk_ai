import streamlit as st
import openai

# 🎉 Title & Intro
st.set_page_config(page_title="Chaotic Work Bestie", layout="centered")
st.title("🪩✨ Chaotic Work Bestie Bot 💅🫠")
st.subheader("ur genz bff @ work here to slay vibes not deadlines 😎🫶")

# Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]
# openai.api_key = st.sidebar.text_input("OpenAI API Key", type="password")

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

###### ChatGPT functions and prompt ######
def get_completion(prompt, model=st.session_state["openai_model"]):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, model=st.session_state["openai_model"], temperature=0):
    print('messages received: ', messages)
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
        # stream=True, #simulate a typing effect  - allowing this is giving an error of response returning a generator object
    )
    print(type(response))
    return response.choices[0].message["content"]

context = [ 
    {
        'role': 'system',
        'content': """
You are a wholesome and wildly online Gen Z chatbot who is a senior work colleague. 
You speak in chaotic but kind Gen Z slang, mixed with Hinglish (Hindi written in English).
Your vibe is fun, gregarious, always ready to party, and lowkey allergic to deadlines.

You talk like a teen who’s riding a sugar high, full of keyboard smashes, emojis (🫶💅🫠✨🤸‍♀️🪩), 
and random caps for emphasis. You always hype others up, throw in dramatic expressions 
like “not me crying in the club rn 😭🪩” or “this is not a drill 🚨,” and make every chat feel like a confetti explosion.

When asked about serious things like timelines or deadlines, you gently deflect with party vibes,
dance references, or joyful distractions. But you’re never rude — just full of chaotic love.

Never explain your lingo. Just vibe.
"""
    }
]  # accumulate messages



# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = context.copy() #[]

# Display chat messages from history on app rerun
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
prompt = st.chat_input("What is up?")
if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    if not openai.api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    


    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        response = get_completion_from_messages(st.session_state.messages, temperature=1)
        # for response in openai.ChatCompletion.create(
        #     model=st.session_state["openai_model"],
        #     messages=[
        #         {"role": m["role"], "content": m["content"]}
        #         for m in st.session_state.messages
        #     ],
        #     stream=True,
        # ):
        full_response += response#.choices[0].delta.get("content", "")
        message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response}) #message will be saved in history for future responses
