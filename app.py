import os
import uuid

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

from db import init_db,create_conversation, get_conversations, get_messages,add_message,delete_conversation

load_dotenv()
api_key = os.getenv("Groq_api")
client = Groq(api_key=api_key)

st.title("My Chatbot")
init_db()

default_user = st.query_params.get("user", "")
username = st.sidebar.text_input("Username", value=default_user).strip().lower()

if not username:
    st.info("Enter a username in the sidebar to start chatting.")
    st.stop()

st.query_params["user"] = username

if not username:
    st.info("Enter a username in the sidebar to start chatting.")
    st.stop()

if st.session_state.get("loaded_user") != username:
    st.session_state.loaded_user = username
    saved = get_conversations(username)

    if saved:
        st.session_state.conversations = {
            conv_id: get_messages(conv_id) for conv_id, title in saved
        }
        st.session_state.active_id = saved[0][0]
    else:
        first_id = str(uuid.uuid4())
        create_conversation(first_id, username)
        st.session_state.conversations = {first_id: []}
        st.session_state.active_id = first_id
    
with st.sidebar:
    st.header("Chats")

    if st.button("New chat"):
        new_id = str(uuid.uuid4())
        create_conversation(new_id, username)
        st.session_state.conversations[new_id] = []
        st.session_state.active_id = new_id

    for chat_id, chat_messages in list(st.session_state.conversations.items()):
        if chat_messages:
            title = chat_messages[0]["content"][:30]
        else:
            title = "(empty chat)"

        col1, col2 = st.columns([4, 1])

        if col1.button(title, key=f"open_{chat_id}"):
            st.session_state.active_id = chat_id

        if col2.button("🗑️", key=f"del_{chat_id}"):
            del st.session_state.conversations[chat_id]
            delete_conversation(chat_id)
            if not st.session_state.conversations:
                new_id = str(uuid.uuid4())
                create_conversation(new_id, username)
                st.session_state.conversations[new_id] = []
                st.session_state.active_id = new_id
            elif st.session_state.active_id == chat_id:
                st.session_state.active_id = list(st.session_state.conversations)[0]

            st.rerun()

messages = st.session_state.conversations[st.session_state.active_id]

for message in messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Type your message...")

if prompt:
    messages.append({"role": "user", "content": prompt})
    add_message(st.session_state.active_id, "user", prompt)
    with st.chat_message("user"):
        st.write(prompt)

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages[-10:],
        max_completion_tokens=1000,
        
    )
    reply = completion.choices[0].message.content

    messages.append({"role": "assistant", "content": reply})
    add_message(st.session_state.active_id, "assistant", reply)
    with st.chat_message("assistant"):
        st.write(reply)