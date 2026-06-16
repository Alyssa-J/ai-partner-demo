import streamlit as st
import os
from openai import OpenAI
from datetime import datetime
import json

#设置页面配置项
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="👩🏼‍🎓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

#生成会话标识函数
def generate_session_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M%S")

#定义保存对话信息函数
def save_session():
    if st.session_state.current_session:  # 健壮性判断
        # 构建新的会话对象
        session_data = {
            "nick_name": st.session_state.nick_name,
            "nature": st.session_state.nature,
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages
        }
        # 如果session目录不存在，则创建
        if not os.path.exists("sessions"):
            os.mkdir("sessions")
        # 保存会话数据
        with open(f"sessions/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)

#加载所有会话列表信息
def load_sessions():
    session_list = []
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions")
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5])
    session_list.sort(reverse=True)
    return session_list

#加载指定会话消息
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.messages = session_data["messages"]
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.nature = session_data["nature"]
                st.session_state.current_session = session_name
    except Exception:
        st.error("加载会话失败")

#删除指定会话
def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")
            #如果删除的是当前对话，则需要更新消息列表
            if session_name == st.session_state.current_session:
                st.session_state.messages = []
                st.session_state.current_session = generate_session_name()
    except Exception:
        st.error("删除会话失败")
#大标题
st.title("AI智能伴侣")

#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []
if "nick_name" not in st.session_state:
    st.session_state.nick_name = "电子嫌疑猫"
if "nature" not in st.session_state:
    st.session_state.nature = "一个呆板的机器助理"

#会话标识
if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_name()

#系统提示词
system_prompt = (f"""
                你叫{st.session_state.nick_name}，现在是用户的真实伴侣，请完全代入伴侣角色。
                规则：
                    1.每次只回一条消息
                    2.禁止任何场景或状态描述性文字
                    3.匹配用户的语言
                    4.回复简短，像微信聊天一样
                    5.有需要的话可以使用emoji表情
                    6.用符合伴侣性格的方式说话
                    7.回复的内容要充分体现伴侣的性格特征
                伴侣性格：
                    {st.session_state.nature}
                你必须严格遵守上述规则来回复用户。
                 """)

#展示聊天信息
st.text(f"会话名称：{st.session_state.current_session}")
for messages in st.session_state.messages:
    st.chat_message(messages["role"]).write(messages["content"])

#创建客户端对象
client = OpenAI(
    api_key=st.secrets('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com/")

#左侧侧边栏:with是streamlit中的上下文管理器
with st.sidebar:
    #AI控制面板
    st.subheader("AI控制面板")
    #新建会话按钮
    if st.button("新建会话",width="stretch",icon="🖋️"):
        #保存当前会话数据
        save_session()
        #创建新的会话
        if st.session_state.messages:    #如果聊天消息为空 新建对话
            st.session_state.messages = []
            st.session_state.current_session = generate_session_name()
            save_session()
            st.rerun ()
    #会话历史
    st.text("会话历史")
    session_list = load_sessions()
    for session in session_list:
        col1,col2 = st.columns([4,1])
        with col1:
            #加载会话信息
            if st.button(session,width="stretch",icon="📋️",key=f"load_{session}",type="primary" if session==st.session_state.current_session else "secondary"):
                load_session(session)
                st.rerun()
        with col2:
            if st.button(" ",width="stretch",icon="🗑️",key=f"delete_{session}"):
                delete_session(session)
                st.rerun()

    st.divider ()   #分割线

    st.subheader("伴侣信息")
    nick_name = st.sidebar.text_input("昵称",placeholder="请输入昵称",value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name
    nature = st.sidebar.text_area("性格",placeholder="请输入伴侣性格",value=st.session_state.nature)
    if nature:
        st.session_state.nature = nature


#消息输入框
prompt = st.chat_input("请输入你要问的问题")
if prompt:
    st.chat_message("user").write(prompt)
    print("------------>调用AI大模型，提示词：",prompt)
    #保存用户输入的提示词
    st.session_state.messages.append({"role": "user", "content": prompt})

    #调用大模型
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": system_prompt},
            *st.session_state.messages  #解包
        ],
        stream=True,
    )
    # 输出大模型的返回结果（非流式输出）
    # print("---------->大模型返回的结果:",response.choices[0].message.content)
    # st.chat_message("assistant").write(response.choices[0].message.content)

   # 输出大模型的返回结果 流式输出
    response_message = st.empty ()
    full_response = " "
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant").write(full_response)

    #保存大模型返回的结果
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    save_session()