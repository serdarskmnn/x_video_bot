from gtts import gTTS
import os
import asyncio

class AudioGenerator:
    def __init__(self, lang="tr"):
        self.lang = lang

    async def generate_audio(self, text, output_path):
        """
        Google TTS kullanarak metni sese çevirir.
        """
        # Google mp3 çıktısı verir
        if output_path.endswith(".wav"):
            output_path = output_path.replace(".wav", ".mp3")
            
        print(f"🎤 Ses işleniyor (Google TTS)...")
        
        if os.path.exists(output_path):
            os.remove(output_path)

        try:
            # Metni sese çevir
            tts = gTTS(text=text, lang=self.lang, slow=False)
            tts.save(output_path)
            
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"✅ Ses dosyası hazır: {output_path}")
                return output_path
            else:
                print("❌ Hata: Ses dosyası oluşturulamadı.")
                return None
        except Exception as e:
            print(f"❌ Ses Hatası: {e}")
            return None