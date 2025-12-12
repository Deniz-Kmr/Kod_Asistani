import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()


api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("❌ API Anahtarı bulunamadı! Lütfen .env dosyasını kontrol et.")
    st.stop() 

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')


st.set_page_config(page_title="Kod Asistanı", page_icon="💻", layout="wide")


st.title("💻 Kod Asistanı")
st.markdown("Hangi dilde yardıma ihtiyacın varsa seç, sorunu yaz, **Yapay Zeka** halletsin.")
st.divider() 


with st.sidebar:
    st.header("⚙️ Ayarlar")
    selected_language = st.selectbox(
        "Hangi dilde kod istiyorsun?",
        ["Python", "C#", "Flutter (Dart)", "JavaScript", "SQL", "Java", "HTML/CSS"]
    )
    st.info(f"Seçilen Dil: **{selected_language}**")


col1, col2 = st.columns([2, 1]) 

with col1:
    user_question = st.text_area("Sorunu buraya yaz:", height=150, placeholder="Örnek: Bir listedeki çift sayıları bulan fonksiyon yaz...")

    if st.button("🚀 Kodu Üret", use_container_width=True):
        if not user_question:
            st.warning("Lütfen önce bir soru yaz.")
        else:
            with st.spinner("Yapay zeka düşünüyor... 🧠"):
                try:
                    prompt = f"""
                    Sen uzman bir yazılımcısın. Aşağıdaki isteği yerine getir.
                    
                    Hedef Dil: {selected_language}
                    Kullanıcı Sorusu: {user_question}
                    
                    Lütfen cevabı şu formatta ver:
                    1. Önce kısa bir açıklama yap.
                    2. Ardından çalışan temiz kodu ver.
                    3. Kodun ne yaptığını adım adım Türkçe açıkla.
                    """
                
                    response = model.generate_content(prompt)
        
                    st.success("İşlem Başarılı! İşte cevabın:")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Bir hata oluştu: {e}")

with col2:
    
    st.markdown("### 💡 İpuçları")
    st.write(f"- Şu an **{selected_language}** modundasın.")
    st.write("- Sorunu ne kadar net yazarsan o kadar iyi cevap alırsın.")
    st.write("- Hata mesajı alıyorsan sorunun sonuna 'Hata veriyor' diye ekle.")

    st.markdown("---")
    st.caption("🚀 Geliştirici: Deniz Çelik | Powered by Google Gemini 2.5")