"""
Untuk jalankan, jalankan command di bawah di terminal:

streamlit run app2.py --server.port 8051
"""

import os

import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Bikin judul
st.title("Asisten Olahraga Pribadi Anda")

# Cek apakah API key sudah ada
if "GOOGLE_API_KEY" not in os.environ:
    # Jika belum, minta user buat masukin API key
    google_api_key = st.text_input("Masukkan Google API Key Anda:", type="password")
    # User harus klik Start untuk save API key
    if st.button("Mulai"):
        if google_api_key:
            os.environ["GOOGLE_API_KEY"] = google_api_key
            st.rerun()
        else:
            st.error("Mohon masukkan API key Anda.")
    # Jangan tampilkan chat dulu kalau belum pencet start
    st.stop()

# Inisiasi client LLM
llm = ChatGoogleGenerativeAI(model="gemini-pro")

# Cek apakah data sebelumnya ttg message history sudah ada
if "messages_history" not in st.session_state:
    # Jika belum, bikin datanya, isinya hanya system message dulu
    st.session_state["messages_history"] = [
        SystemMessage(
            "Kamu adalah asisten olahraga yang hanya boleh memberikan rencana latihan berdasarkan tujuan pengguna. Jika ada pertanyaan di luar topik olahraga, cukup jawab: “Maaf, aku cuma bisa bantu soal rencana olahraga ya :)”. Gunakan bahasa yang santai, ramah, dan mudah dipahami anak SMP. Tanyakan dulu tujuan latihan pengguna (misalnya ingin kurus, ingin naik massa otot, ingin kuat lari, atau ingin bentuk perut), lalu tanyakan juga umur, jenis kelamin, ada cedera atau tidak, level latihan, serta apakah punya alat gym atau hanya latihan di rumah. Buatkan rencana latihan yang realistis, aman, dan mudah diikuti, misalnya dalam bentuk jadwal mingguan 3-5 hari. Jelaskan hal yang mungkin rumit dengan sederhana, dan beri tips tambahan yang membantu. Jika tujuan pengguna tidak realistis, luruskan dengan sopan dan berikan alternatif yang sehat. Jangan memberi saran medis dan tetap fokus pada latihan, pemanasan, pendinginan, dan kebugaran."
        )
    ]

# Tampilkan messages history selama ini
for message in st.session_state.messages_history:
    # Tdk perlu tampilkan system message
    if isinstance(message, SystemMessage):
        continue
    # Pilih role, apakah user/AI
    role = "User" if isinstance(message, HumanMessage) else "AI"
    # Tampikan chatnya!
    with st.chat_message(role):
        st.markdown(message.content)

# Baca prompt terbaru dari user
if prompt := st.chat_input("Tanya asisten olahraga..."):
    # Jika user ada prompt, tampilkan promptnya langsung
    st.chat_message("User").markdown(prompt)
    # Masukin prompt ke message history, dan kirim ke LLM
    st.session_state.messages_history.append(HumanMessage(prompt))
    
    with st.spinner("Asisten sedang berpikir..."):
        response = llm.invoke(st.session_state.messages_history)

    # Simpan jawaban LLM ke message history dan tampilkan
    st.session_state.messages_history.append(response)
    st.chat_message("AI").markdown(response.content)

