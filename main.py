import streamlit as st

from langchain.memory import ConversationBufferMemory
import os

st.title("⚪克隆ChatGPT")

from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory


def get_chat_response(prompt, memory, model_name, openai_api_key, openai_api_base):
    model = ChatOpenAI(model=model_name, openai_api_key=openai_api_key, openai_api_base=openai_api_base)
    chain = ConversationChain(llm=model, memory=memory)

    response = chain.invoke({"input": prompt})  ##这是一串字典
    print(response)
    return response["response"]  ##但是只用返回回应即可


with st.sidebar:
    openai_api_key = st.text_input("请输入OpenAI API密钥：")
    openai_api_base = st.text_input("请输入AI的Base Url：", "https://api.gpts.vin/v1")
    model_name = st.selectbox("选择翻译模型", ["gpt-3.5-turbo", "gpt-4o", "gpt-4", "gpt-4-1106-preview"])
    st.markdown("[获取OpenAI API密钥](https://platform.openai.com/account/api-keys)")
    st.markdown("[国内的可以用智谱AI API密钥（推荐）](https://open.bigmodel.cn/overview)")

    clean = st.button("清空聊天记录")


def clear_merroy_and_message():
    if "memory" in st.session_state:
        del st.session_state["memory"]
    if "messages" in st.session_state:
        del st.session_state["messages"]


if clean:
    clear_merroy_and_message()

if "memory" not in st.session_state:  ##如果memory不在会话状态里，那么就创建新记忆
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
    st.session_state["messages"] = [{"role": "AI",
                                     "content": "你好，我是AI助手，有什么我可以帮您的？"}]

for message in st.session_state["messages"]:  # 迭代消息内容，让每条消息都展示出来
    st.chat_message(message["role"]).write(message["content"])
    # st.chat_message() 用于在 Streamlit 应用程序中创建聊天消息样式的显示区域。

prompt = st.chat_input()
if prompt:
    if not openai_api_key:
        st.info("请输入你的OpenAI API KEY")
        st.stop()
    st.session_state["messages"].append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)
    with st.spinner("AI正在思考中，请稍等……"):
        response = get_chat_response(prompt,
                                     st.session_state["memory"],
                                     model_name,
                                     openai_api_key,
                                     openai_api_base)
    msg = {"role": "ai", "content": response}
    st.session_state["messages"].append(msg)
    st.chat_message("ai").write(response)
