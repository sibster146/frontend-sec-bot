import streamlit as st
import requests
import urllib.parse
import extra_streamlit_components as stx
import uuid
import json

def get_response(prompt, cookie_value):
    try:
        base_url = "https://ztwheo6lrfirvfzlkyuvliu7zy0eibve.lambda-url.us-east-1.on.aws/"
        params = {
            "query": prompt,
            "cookie_value": cookie_value
        }
        encoded_params = urllib.parse.urlencode(params)
        full_url = f"{base_url}?{encoded_params}"
        response = requests.get(full_url)
        return response.content.decode('utf-8').replace("\\n", "\n").replace("\\'", "'")
    except Exception as e:
        return str(e)
    

def button_function(index):
    try:
        base_url = "https://mrb3e6ksffm24bfxa2jtevm5xy0thpfl.lambda-url.us-east-1.on.aws/"
        
        ai_message = st.session_state.messages[index]
        ai_content = ai_message["content"]
        human_message = st.session_state.messages[index-1]
        human_content = human_message["content"]
        data = {"completion": ai_content,"prompt":human_content}
        datajson = json.dumps(data)
        params = {
            "data": datajson
        }
        encoded_params = urllib.parse.urlencode(params)
        full_url = f"{base_url}?{encoded_params}"
        response = requests.get(full_url)
        return response.status_code
    except Exception as e:
        print(e)
        return str(e)


cookie_manager = stx.CookieManager()
cookies = cookie_manager.get_all()
cookie_name = 'user_session'
cookie_value = cookies.get(cookie_name, None)

st.title("Security Bot (RAG)")

# Initialize session state list if it doesn't exist
if 'messages' not in st.session_state:
    st.session_state.messages = []

# If new text is input, append it to the session state list
prompt = st.chat_input("I'm still a work in progress! Please be as specific as possible :))")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

if cookie_value is None:
    cookie_value = str(uuid.uuid4())
    cookie_manager.set(cookie=cookie_name, val=cookie_value)

for i, message in enumerate(st.session_state.messages):
    role = message["role"]
    content = message["content"]
    if not content:
        continue
    height = max(100, min(len(content) * 2, 500))
    with st.chat_message(role):
        if role == "assistant":
            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                button_key = f'button_{i}'

                if st.session_state.messages[i]["button_pressed"]:
                    st.button("Done", disabled=True, key=f"done_button_{i}")
                else:
                    if st.button("Push", key=button_key):
                        if button_function(i) == 200:
                            st.session_state.messages[i]["button_pressed"] = True
                            st.rerun()
            with col2:
                edited_text = st.text_area(
                    role, 
                    value=content, 
                    key=f"message_{i}",
                    height=height
                )
                st.session_state.messages[i]["role"] = role
                st.session_state.messages[i]["content"] = edited_text
                
        else:
            edited_text = st.text_area(
                role, 
                value=content, 
                key=f"message_{i}",
                height=height
            )
            st.session_state.messages[i]["role"] = role
            st.session_state.messages[i]["content"] = edited_text

if prompt:
    response = get_response(prompt, cookie_value)
    st.session_state.messages.append({"role": "assistant", "content": response,"button_pressed":False})
    st.rerun()
