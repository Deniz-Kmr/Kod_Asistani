import os
from dotenv import load_dotenv
import google.generativeai as genai


def configure_genai():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return False, "❌ API Anahtarı bulunamadı! .env dosyasını kontrol et."
    
    genai.configure(api_key=api_key)
    return True, "Bağlantı Başarılı"


model = genai.GenerativeModel('gemini-2.5-flash')


def ask_gemini(prompt, language, mode):
    try:
       
        if mode == "Kod Yazma":
            system_instruction = f"Sen uzman bir {language} geliştiricisisin. İsteğe uygun çalışan kod yaz ve kodun ne yaptığını kısaca açıkla."
        elif mode == "Hata Ayıklama (Debug)":
            system_instruction = f"Sen bir debug uzmanısın. {language} dilindeki bu koddaki hataları bul, düzelt ve nedenini adım adım anlat."
        else: 
            system_instruction = f"Bu {language} kodunu her satırını detaylıca, bir öğrenciye anlatır gibi açıkla. Mantığını öğret."

        full_prompt = f"{system_instruction}\n\nKullanıcı İsteği: {prompt}"
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Hata oluştu: {str(e)}"


def get_file_extension(language):
    ext_map = {
        "Python": "py", "C#": "cs", "Flutter (Dart)": "dart",
        "JavaScript": "js", "SQL": "sql", "Java": "java",
        "C++": "cpp", "HTML/CSS": "html"
    }
    return ext_map.get(language, "txt")