import streamlit as st
import openai

# 🎉 Title & Intro
st.set_page_config(page_title="Chaotic Work Bestie", layout="centered")
st.title("🪩✨ Chaotic Work Bestie Bot 💅🫠")
st.subheader("ur genz bff @ work here to slay vibes not deadlines 😎🫶")

# 🎨 Custom CSS for chat bubbles & vibe
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #fff0f5, #e0f7fa);
        color: #2b2b2b;
        font-family: "Comic Sans MS", cursive, sans-serif;
    }
    .stMarkdown {
        font-size: 1.1rem;
        line-height: 1.6;
    }
    .chat-message {
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# 🔐 Set API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 💬 OpenAI Call Helpers
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=1):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]

# 🧠 Set context
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
]

# 🧾 Chat History Setup
if "messages" not in st.session_state:
    st.session_state.messages = context.copy()

# 📜 Expandable helper section
with st.expander("❓ what can u ask me"):
    st.markdown("""
    - “what's the vibe today?”
    - “how do I handle this deadline?”
    - “should I go to that boring meeting?”
    - “give me a hype up speech pls”
    """)

# 📚 Display past messages
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        avatar = "👩‍💻" if message["role"] == "user" else "🪩"
        bubble_color = "#fce4ec" if message["role"] == "user" else "#e0f7fa"
        st.markdown(
            f"<div style='background-color:{bubble_color}; padding:10px; border-radius:10px;'>{avatar} {message['content']}</div>",
            unsafe_allow_html=True
        )

# 📥 Input & Response Logic
prompt = st.chat_input("what’s the vibe? 🧃")
if prompt:
    # User msg
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Typing response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("✨ typing like my nails depend on it... 💅▌")
        response = get_completion_from_messages(st.session_state.messages, temperature=1)
        message_placeholder.markdown(response)

    # Store bot msg
    st.session_state.messages.append({"role": "assistant", "content": response})

    # 🎈 Fun effects
    if any(word in response.lower() for word in ["party", "slay", "delulu", "confetti"]):
        st.balloons()
    if "delulu" in response.lower():
        st.snow()
