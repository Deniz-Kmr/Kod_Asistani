import streamlit as st
import time
import logic
import streamlit.components.v1 as components 

st.set_page_config(page_title="Pro Kod Asistanı", page_icon="💻", layout="wide")

def local_css(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

local_css("style.css")


status, message = logic.configure_genai()
if not status:
    st.error(message)
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0
if "estimated_tokens" not in st.session_state:
    st.session_state.estimated_tokens = 0

with st.sidebar:
    try:
        st.image("image/kodasistanı.png", use_container_width=True)
    except Exception:
        st.warning("⚠️ Logo bulunamadı. Yol: image/kodasistanı.png")

    st.title("🛠️ Kontrol Paneli")
    st.markdown("---")
    
    app_mode = st.selectbox("Çalışma Modu:", ["Kod Yazma", "Hata Ayıklama (Debug)", "Kod Açıklama"])
    
    selected_language = st.selectbox(
        "Programlama Dili:", 
        ["HTML/CSS/JS (Web)", "Python", "Flutter (Dart)", "Kotlin", "Swift", "C#", "SQL", "Java", "JavaScript", "C++"]
    )
    
    st.divider()


    st.markdown("📊 **Kullanım İstatistikleri**")
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("Toplam Soru", st.session_state.usage_count)
    with col_stat2:
        st.metric("Tahmini Token", st.session_state.estimated_tokens)
    
    st.progress(min(st.session_state.usage_count * 10, 100), text="Günlük Limit Durumu")
    
    st.divider()
    
    st.markdown(f"""
    <div style="background-color:#1e2129; padding:12px; border-radius:8px; border:1px solid #444;">
        📍 <strong style="color:#FF914D">Mod:</strong> {app_mode}<br>
        🎯 <strong style="color:#FF914D">Dil:</strong> {selected_language}
    </div>
    """, unsafe_allow_html=True)

    if "Web" in selected_language:
        st.success("🌐 Canlı Önizleme Aktif")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🗑️ Sohbeti Temizle", use_container_width=True):
        st.session_state.messages = []
        st.session_state.usage_count = 0 
        st.session_state.estimated_tokens = 0
        st.rerun() 
    
    st.caption("Geliştirici : Deniz Çelik")


st.title("</> Pro Kod Asistanı")

if "Web" in selected_language:
    st.caption("✨ HTML/CSS modundasınız. Kodlarınız sağ tarafta canlı önizlenecek.")
else:
    st.caption(f"🚀 {selected_language} geliştirme modundasınız.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Kod iste..."):
    st.session_state.usage_count += 1
    st.session_state.estimated_tokens += (len(prompt) + 100) // 2 

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"{selected_language} kodu yazılıyor..."):
            full_response = logic.ask_gemini(prompt, selected_language, app_mode)
    
            if "Web" in selected_language:
                tab1, tab2 = st.tabs(["📝 Kod & Açıklama", "👁️ Canlı Önizleme"])
                
                with tab1:
                    st.markdown(full_response)
                    st.download_button("📥 İndir", full_response, "index.html")
                
                with tab2:
                    st.success("⚡ Tarayıcı Çıktısı:")
                    html_code = full_response
                    if "```html" in full_response:
                        try:
                            html_code = full_response.split("```html")[1].split("```")[0]
                        except:
                            pass 
                    components.html(html_code, height=500, scrolling=True)
            
            else:
                st.markdown(full_response)
                file_ext = logic.get_file_extension(selected_language)
                st.download_button(
                    label=f"📥 {selected_language} Dosyasını İndir",
                    data=full_response,
                    file_name=f"kod_asistani_{int(time.time())}.{file_ext}"
                )

    st.session_state.messages.append({"role": "assistant", "content": full_response})