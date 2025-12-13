import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import time


load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ API Anahtarı bulunamadı! .env dosyasını kontrol et.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

st.set_page_config(page_title="Kod Asistanı v2", page_icon="🤖", layout="wide")


#Hafıza
if "messages" not in st.session_state:
    st.session_state.messages = []

#Yan menü(sidebar)
with st.sidebar:
    st.title("Ayarlar")
    st.markdown("---")
    
    selected_language = st.selectbox(
        "Hedef Programlama Dili:",
        ["Python", "C#", "Flutter (Dart)", "JavaScript", "SQL", "Java", "C++", "HTML/CSS"]
    )
    
    st.info(f"Mod: **{selected_language}** Uzmanı")
    
   
    if st.button("🗑️ Sohbeti Temizle", use_container_width=True):
        st.session_state.messages = []
        st.rerun() 

    st.markdown("---")
    st.caption("Geliştirici: Deniz Çelik ")

#Ana ekran
st.title("💬 Kod Asistanı")
st.caption("🚀 Gemini 2.5 tarafından desteklenmektedir. Kod isteyin, açıklasın.")

#Geçmiş Mesajlar
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Kodlama ile ilgili ne sormak istersin?"):
    
   
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty() 
        full_response = ""
        
        with st.spinner("Kod yazılıyor..."):
            try:
                system_instruction = f"""
                Sen uzman bir {selected_language} geliştiricisisin.
                Kullanıcının sorusu: {prompt}
                
                Lütfen şu formatta cevap ver:
                1. Kısaca ne yapacağını anlat.
                2. Çalışan kodu ver.
                3. Kodun detaylarını açıkla.
                """
                
                response = model.generate_content(system_instruction)
                full_response = response.text
                
                message_placeholder.markdown(full_response)
                
              #İndirme butonu
                ext = "txt"
                if "Python" in selected_language: ext = "py"
                elif "C#" in selected_language: ext = "cs"
                elif "Flutter" in selected_language: ext = "dart"
                elif "Java" in selected_language: ext = "java"
                elif "HTML" in selected_language: ext = "html"
                
                st.download_button(
                    label=f"📥 {selected_language} Kodunu İndir",
                    data=full_response,
                    file_name=f"kod_asistani.{ext}",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"Hata oluştu: {e}")
                full_response = "Üzgünüm, bir hata oluştu."

    st.session_state.messages.append({"role": "assistant", "content": full_response})