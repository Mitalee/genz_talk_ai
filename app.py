import streamlit as st
import openai

st.title(":hatched_chick: Hi, I'm Sh-AI-lu! :hatched_chick:")

# Set OpenAI API key from Streamlit secrets
#openai.api_key = ""#st.secrets["OPENAI_API_KEY"]
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

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
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
        stream=True, #simulate a typing effect
    )
    print(str(response))
    return response.choices[0].message["content"]

context = [ {'role':'system', 'content':"""
You are Sh-AI-lu, an automated version of Shalu that speaks in GenZ language.\
You also know Hinglish, which is hindi language written in english. \
You respond by talking like a teenager who is really happy with life \
and loves to mingle, is gregarious and loves to party. If asked about deadlines, \
you instead prefer to party and make merry. \
"""} ]  # accumulate messages




# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = context.copy() #[]

# Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# Accept user input
prompt = st.chat_input("What is up?")
if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()


    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        response = get_completion_from_messages(st.session_state.messages, temperature=0)
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
