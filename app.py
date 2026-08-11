import streamlit as st
from llm_agent import process_request

st.set_page_config(page_title="Bursa Trafik Analizi", page_icon="🚦", layout="centered")

st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
        }
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        .welcome-container {
            text-align: center;
            margin-top: 10vh;
            margin-bottom: 5vh;
        }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🚦 Trafik Asistanı")
    st.caption("Bursa saatlik trafik yoğunluk verileri")
    if st.button("➕ Yeni Sohbet", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    st.markdown(
        '''
        <div class="welcome-container">
            <h1>🚦 Bursa Trafik Analizi</h1>
            <p style="color: gray;">Yola çıkmadan önce saatlik trafik yoğunluğunu sorun.</p>
        </div>
        ''', 
        unsafe_allow_html=True
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Trafik durumunu sor (Örn: Yarın sabah 8'de çıksam mantıklı mı?)"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Trafik verileri analiz ediliyor..."):
            cevap = process_request(prompt)
            st.markdown(cevap)
            
    st.session_state.messages.append({"role": "assistant", "content": cevap})