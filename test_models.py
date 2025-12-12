import google.generativeai as genai
import os
from dotenv import load_dotenv

# Şifreyi yükle
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("HATA: API Key bulunamadı!")
else:
    try:
        genai.configure(api_key=api_key)
        
        print("\n--- Hesaptaki Modeller---")
        found = False
        for m in genai.list_models():
            # Sadece 'text' üretebilen modelleri bul
            if 'generateContent' in m.supported_generation_methods:
                print(f"+ İsim: {m.name}")
                found = True
        
        if not found:
            print(" Model Bulunamadı")
            
    except Exception as e:
        print(f"HATA OLUŞTU: {e}")