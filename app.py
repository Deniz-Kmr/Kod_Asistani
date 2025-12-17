import streamlit as st
import time
import logic  


st.set_page_config(page_title="Pro Kod Asistanı v3", page_icon="💻", layout="wide")


status, message = logic.configure_genai()
if not status:
    st.error(message)
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:
    st.title("🛠️ Geliştirici Paneli")
    st.markdown("---")
    
    app_mode = st.selectbox("Çalışma Modu:", ["Kod Yazma", "Hata Ayıklama (Debug)", "Kod Açıklama"])
    selected_language = st.selectbox("Programlama Dili:", ["Python", "C#", "Flutter (Dart)", "JavaScript", "SQL", "Java", "C++", "HTML/CSS"])
    
    st.divider()
    st.info(f"📍 **Mod:** {app_mode}\n\n🎯 **Dil:** {selected_language}")
    
    if st.button("🗑️ Sohbeti Temizle", use_container_width=True):
        st.session_state.messages = []
        st.rerun() 
    
    st.markdown("---")
    st.caption("🚀 Geliştirici: Deniz Çelik | v3.0")


st.title("💬 Pro Kod Asistanı v3")


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Kod iste veya hatanı yapıştır..."):
    
   
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

   
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner(f"{app_mode} yapılıyor..."):
            
           
            full_response = logic.ask_gemini(prompt, selected_language, app_mode)
            
            
            message_placeholder.markdown(full_response)
            
            
            file_ext = logic.get_file_extension(selected_language)
            st.download_button(
                label=f"📥 {selected_language} Dosyasını İndir",
                data=full_response,
                file_name=f"kod_asistani_{int(time.time())}.{file_ext}",
                mime="text/plain"
            )

    st.session_state.messages.append({"role": "assistant", "content": full_response})