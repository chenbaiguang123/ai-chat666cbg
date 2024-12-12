import streamlit as st
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
api_key = os.getenv("HF_API_KEY")

# 设置页面标题
st.title(" 杨司令的私人助手")

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示聊天历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入
if prompt := st.chat_input("在这里输入你的问题..."):
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 添加到聊天历史
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # 创建 HuggingFace 客户端
        client = InferenceClient(
            model="Qwen/QwQ-32B-Preview",
            token=api_key
        )
        
        # 获取 AI 响应
        completion = client.chat.completions.create(
            messages=st.session_state.messages,
            max_tokens=500,
            temperature=0.7,
            top_p=0.95
        )

        # 显示 AI 响应
        with st.chat_message("assistant"):
            ai_response = completion.choices[0].message.content
            st.markdown(ai_response)
        
        # 添加到聊天历史
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

    except Exception as e:
        st.error(f"发生错误: {str(e)}")