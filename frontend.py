import streamlit as st
from streamlit.elements.write import StreamingOutput
import requests
import urllib.parse

st.title("Security Bot (RAG)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    base_url = "https://ztwheo6lrfirvfzlkyuvliu7zy0eibve.lambda-url.us-east-1.on.aws/"
    params = {
        "query": prompt
    }
    encoded_params = urllib.parse.urlencode(params)
    full_url = f"{base_url}?{encoded_params}"
    with st.chat_message("assistant"):
        stream = requests.get(full_url,stream=True)
        complete_text_list = []
        for chunk in stream.iter_content(chunk_size = 1024):
            if chunk:
                text = chunk.decode('utf-8').replace("\\n","\n").replace("\\'","'")
                st.markdown(text)
                complete_text_list.append(text)
    complete_text_string = "".join(complete_text_list)
    st.session_state.messages.append({"role": "assistant", "content": complete_text_string})

# https://frontend-sec-bot-rmdsnhyfgevmsb2beohlhh.streamlit.app/
