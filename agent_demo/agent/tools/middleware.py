import time
import re

import streamlit as st
from agent.react_agent import ReactAgent
from agent.tools.api_user_location import api_city

city_info = api_city()

st.title("智能扫地机器人客服")
st.divider()

# 创建智能助手
if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

# 会话记录
if "message" not in st.session_state:
    st.session_state["message"] = []

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 用户输入提示词
prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})
    response_messages = []


    # 过滤 JSON 内容的函数
    def filter_json_content(text):
        """过滤掉 JSON 格式的内容，只保留友好文本"""
        # 匹配大括号包裹的 JSON 对象
        json_pattern = r'\{[^{}]*\}'
        # 如果文本包含 JSON 特征（大括号、引号、冒号的组合），则过滤掉
        if re.search(json_pattern, text) and ('"' in text or ':' in text):
            return None
        return text


    with st.spinner("智能客户思考中..."):
        res_stream = st.session_state["agent"].execute_stream(prompt)


        def capture(generator, cache_list):
            for chunk in generator:
                # 过滤掉 JSON 内容
                filtered_chunk = filter_json_content(chunk)
                if filtered_chunk:
                    cache_list.append(filtered_chunk)
                    for char in filtered_chunk:
                        time.sleep(0.01)
                        yield char
                    yield filtered_chunk
            # 如果没有有效内容，显示默认回复
            if not cache_list:
                default_response = "已收到您的问题，我正在处理..."
                cache_list.append(default_response)
                yield default_response


        st.chat_message("assistant").write_stream(capture(res_stream, response_messages))
        st.session_state["message"].append({"role": "assistant", "content": response_messages[-1]})
        st.rerun()
