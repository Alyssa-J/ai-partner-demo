import streamlit as st

#页面配置

st.set_page_config(
    page_title="第一个页面",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",   #侧边栏
    menu_items={
        'Get Help': 'https://www.baidu.com',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# 我的入门页面"
    }
)

st.title("Streamlit入门演示")
st.header("一级标题")
st.subheader("二级标题")

#段落文字
st.write("王佳芝本是抗战时期的女大学生，为刺杀汉奸易先生，她假扮阔太“麦太太”以身入局，与同学设下美人计。这场危险的表演让她在精神与肉体上付出惨痛代价——她被迫与厌恶的同学发生关系，又在易先生离沪后沦为无用的弃子。")
st.write("三年后再被同学召回执行任务时，她已彻底沦为易先生的情妇。两人在充满猜忌与暴力的性爱中纠缠，猎人与猎物的界限逐渐模糊。当她从易先生手中接过那颗“鸽子蛋”钻戒时，对方眼中罕见的柔情击溃了她最后的防线，一句“快走”让三年谋划功亏一篑。")
st.write("最终，王佳芝与同伴全部被捕枪决。易先生签下行刑令后，回到太太们的牌桌旁，心中只有劫后余生的庆幸——她不过是“可爱的女人”，而这份“爱”终究成就了他作为冷酷权谋者的又一次胜利。")

#图片
st.image("./resource/微信图片_20260612163140_126_19.jpg",width=200)


#表格
student_data ={
    "姓名":["陈信宏","温尚翊","蔡升晏","石锦航","刘冠佑"],
    "年纪":[50,50,50,51,53]
}
st.table(student_data)

#输入框
name = st.text_input("请输入姓名",type="password")
st.write(f"您输入的姓名：{name}")

#单选按钮
gender = st.radio("请输入您的性别",["男","女"],index=1)
st.write(f"您的性别为：{gender}")