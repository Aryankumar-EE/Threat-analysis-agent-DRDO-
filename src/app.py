import streamlit as st

st.set_page_config(
    page_title="DRDO Intelligent Safety Guard",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>

.main{
background:#071A2E;
}

.big{
font-size:48px;
font-weight:bold;
text-align:center;
color:white;
}

.mid{
font-size:24px;
text-align:center;
color:#7EC8E3;
}

.small{
text-align:center;
color:white;
}

.card{

background:#0E2742;

padding:25px;

border-radius:20px;

border:2px solid #1E88E5;

}

</style>
""",unsafe_allow_html=True)

st.markdown(
'<p class="big">🛡 DRDO Intelligent Safety Guard</p>',
unsafe_allow_html=True
)

st.markdown(
'<p class="mid">AI Powered Multi-Agent Threat Intelligence System</p>',
unsafe_allow_html=True
)

st.markdown(
'<p class="small">Faculty of Technology • University of Delhi</p>',
unsafe_allow_html=True
)

st.divider()

st.info(
"""
👈 Select a portal from the **left sidebar**

👮 Security Officer Portal

or

🖥 Command Center
"""
)

col1,col2,col3=st.columns(3)

col2.image(
"https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
width=250
)

st.divider()

st.markdown("### 🚀 Technologies Used")

c1,c2,c3,c4=st.columns(4)

c1.success("LangGraph")
c2.success("Llama 3.1")
c3.success("FAISS")
c4.success("Streamlit")

st.divider()

st.markdown("### 👨‍💻 Developed By")

st.write("Aryan Kumar")
st.write("Faculty of Technology, University of Delhi")