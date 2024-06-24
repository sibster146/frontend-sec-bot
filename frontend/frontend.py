import streamlit as st
from streamlit.elements.write import StreamingOutput
import requests
import urllib.parse

st.title("Security Bot (RAG)")

if "message" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({
        "role":"user",
        "content": prompt
    })
    with st.chat_message("user"):
        st.markdown(prompt)

    base_url = "https://ztwheo6lrfirvfzlkyuvliu7zy0eibve.lambda-url.us-east-1.on.aws/"
    params = {
        'query':prompt
    }
    encoded_params = urllib.parse.urlencode(params)
    full_url = f"{base_url}?{encoded_params}"
    with st.chat_message("assistant"):
        stream = requests.get(full_url)
        response = st.write_stream(stream)
    st.session_state.messages.append({"role":"assistant","content":response})

