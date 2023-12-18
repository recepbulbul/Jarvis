import win32com.client
import subprocess
import webbrowser
import random
import requests
from bs4 import BeautifulSoup
import json
import speech_recognition as sr

# Türkçe seslendirme motorunu başlat
speaker = win32com.client.Dispatch("SAPI.SpVoice")

# Ses tanıma nesnesini oluşturun
recognizer = sr.Recognizer()

b = input("Lütfen bilgisayarınıza verdiğiniz ismi giriniz: ")

sozluk = {
    "merhaba": ["merhaba size nasıl yardımcı olabilirim?"],
    "nasılsın": ["sormanıza sevindim ama bildiğiniz üzere bir yapay zeka olarak duygulara sahip değilim"],
    "spotify aç": ["Spotify uygulamasını açıyorum....", "Şimdi Spotify'i açıyorum.", "Spotify geliyor!"],
    "spo aç": ["Spotify uygulamasını açıyorum....", "Şimdi Spotify'i açıyorum.", "Spotify geliyor!"],
    "satranç aç": ["Satranç oyununu başlatıyorum....", "Şimdi satranç oyunu başlıyor.", "Satranç geliyor!"],
    "adın nedir": ["Benim ismim Rem size yardımcı olmak için tasarlanmış bir yapay zeka modeliyim"],
    "kaç yaşındasın": ["Yaşımın kaç olduğunu soruyorsanız sanırım bunu bende bilmiyorum :=)"],
    "dünya düz mü": ["Size olan inancımı kaybetmek üzereyim lütfen sizin için açmış olduğum web sitesine göz atın ve inançlarınızı gözden geçirin!"],
    "youtube aç": ["Youtube uygulamasını açıyorum....", "Şimdi Youtube'u açıyorum.", "Youtube geliyor!"],
    "google da arama yapmak istiyorum": ["Tabi ki ne aramak istersiniz?"]
}

with open("sozluk.txt", "r") as dosya:
    sozluk = json.load(dosya)

while True:
    try:
        # Ses girişi alın
        with sr.Microphone() as source:
            print("Lütfen konuşun...")
            audio = recognizer.listen(source)
            print("Ses kaydedildi. Tanıma yapılıyor...")

        # Ses kaydını metne dönüştür
        anahtar = recognizer.recognize_google(audio, language="tr-TR").lower()
        print("Tanınan Metin: " + anahtar)

        en_iyi_eslesme = None

        if anahtar in sozluk:
            en_iyi_eslesme = anahtar  # Tam eşleşme durumunda en iyi eşleşmeyi ayarla
            yanit = random.choice(sozluk[en_iyi_eslesme])
        else:
            anahtar_kelimeler = anahtar.split()

            for kelime in anahtar_kelimeler:
                benzer_anahtarlar = [anahtar for anahtar in sozluk.keys() if kelime in anahtar]
                if benzer_anahtarlar:
                    en_iyi_eslesme = max(benzer_anahtarlar, key=lambda x: len(x))
                    break

            if en_iyi_eslesme:
                yanit = random.choice(sozluk[en_iyi_eslesme])
            else:
                yanit = "Üzgünüm, anlayamadım. Lütfen daha açıklayıcı bir giriş yapın."

        if en_iyi_eslesme:
            if en_iyi_eslesme == "spotify aç" or en_iyi_eslesme == "spo aç":
                spotify_exe_path = rf'C:\Users\{b}\AppData\Roaming\Spotify\Spotify.exe'
                try:
                    subprocess.Popen(spotify_exe_path)
                except Exception as e:
                    yanit = "Spotify açılırken bir hata oluştu: " + str(e)

            if en_iyi_eslesme == "satranç aç":
                url = "https://lichess.org"
                webbrowser.open(url)

            if en_iyi_eslesme == "dünya düz mü":
                url = "https://khosann.com/duz-dunya-teorisini-curuten-12-kanit/"
                webbrowser.open(url)

            if en_iyi_eslesme == "youtube aç":
                url = "https://www.youtube.com/"
                webbrowser.open(url)

            if en_iyi_eslesme == "google da arama yapmak istiyorum":
                try:
                    # Kullanıcıdan sesli bir arama terimi alın
                    with sr.Microphone() as source:
                        print("Arama yapmak istediğiniz terimi söyleyin...")
                        audio = recognizer.listen(source)
                        print("Ses kaydedildi. Arama yapılıyor...")

                    # Ses kaydını metne dönüştür
                    arama_terimi = recognizer.recognize_google(audio, language="tr-TR").lower()
                    print("Aranan Terim: " + arama_terimi)

                    # Google'da arama yap
                    google_url = f"https://www.google.com/search?q={arama_terimi}"
                    webbrowser.open(google_url)

                    # Wikipedia sayfasından bilgi al
                    wikipedia_url = f"https://tr.wikipedia.org/wiki/{arama_terimi.replace(' ', '_')}"
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
                    }
                    sayfa = requests.get(wikipedia_url, headers=headers)
                    soup = BeautifulSoup(sayfa.content, "html.parser")
                    ilk_paragraf = soup.find("p").get_text()
                    sozluk[arama_terimi] = [ilk_paragraf]

                    with open("sozluk.txt", "w") as dosya:
                        json.dump(sozluk, dosya)
                except sr.UnknownValueError:
                    print("Ses anlaşılamadı.")
                except sr.RequestError as e:
                    print("Ses tanıma servisine erişilemiyor: {0}".format(e))

            print("AI:", yanit)
            speaker.Speak(yanit)

    except sr.UnknownValueError:
        print("Ses anlaşılamadı.")
    except sr.RequestError as e:
        print("Ses tanıma servisine erişilemiyor: {0}".format(e))



        print("AI:", yanit)
        speaker.Speak(yanit)
    except sr.UnknownValueError:
        print("Ses anlaşılamadı.")
    except sr.RequestError as e:
        print("Ses tanıma servisine erişilemiyor: {0}".format(e))
