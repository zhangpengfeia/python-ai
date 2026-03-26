'''
ai聊天界面
'''
import time

import streamlit as st

from rag import RagService
import config_data as config

st.title("智能AI")
st.divider()

if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "user", "content": "欢迎来到智能AI，你可以向我提问任何问题。"}]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})
    cache_list=[]
    with st.spinner("思考中..."):
        res_stream = st.session_state["rag"].chain.stream({"input": prompt}, config=config.session_config)
        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk
        st.chat_message("assistant").write_stream(capture(res_stream, cache_list))
        st.session_state["message"].append({"role": "assistant", "content": "".join(cache_list)})