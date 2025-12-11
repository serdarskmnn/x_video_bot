import google.generativeai as genai
import requests
from PIL import Image
from io import BytesIO
import re

class ImageAnalyzer:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = None
        self._find_best_model()

    def _find_best_model(self):
        """Görsel destekli en iyi modeli bulur."""
        print("🔍 AI Modeli seçiliyor...")
        try:
            all_models = list(genai.list_models())
            # Öncelik sırası
            priority = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro-vision']
            
            for p in priority:
                for m in all_models:
                    if p in m.name:
                        self.model = genai.GenerativeModel(m.name)
                        print(f"✅ Model: {m.name}")
                        return
            
            # Bulamazsa son çare
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        except:
            self.model = genai.GenerativeModel('gemini-1.5-flash')

    def analyze_image(self, image_url):
        if not self.model or not image_url: return None

        print(f"🧠 Görseldeki yazılar okunuyor...")

        try:
            # 1. Resmi İndir
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(image_url, headers=headers)
            if response.status_code != 200: return None
            img = Image.open(BytesIO(response.content))

            # 2. STRICT PROMPT (Sıkı Yönerge)
            # AI'ya "Sadece metni ver" diyoruz.
            prompt = """
            GÖREV: Bu resimdeki yazışma metinlerini veya tweet içeriğini sadece sesli okunacak şekilde çıkar.

            KURALLAR:
            1. ASLA yorum yapma (Örn: "Resimde şu var", "Mesajda şöyle diyor" DEME).
            2. ASLA saatleri, tarihleri, pil yüzdesini veya "okundu" bilgilerini yazma.
            3. Emojileri yoksay.
            4. Sadece konuşma balonlarındaki veya ana metindeki saf yazıyı ver.
            5. Diyalog ise sırasıyla oku.
            6. Noktalama işaretlerini (parantez, yıldız vb.) okuma metnine dahil etme.

            Örnek Çıktı Formatı:
            Bilal abi havuç suyu içti çok samimi adam.
            Rasgele harfler.
            """

            # 3. Gemini'ye Gönder
            response = self.model.generate_content([prompt, img])
            
            text = response.text
            if text:
                # TEMİZLİK: AI bazen Markdown (**bold**) kullanır, bunları temizleyelim.
                # Yıldızları, alt çizgileri ve parantez içlerini temizle
                clean_text = text.replace('*', '').replace('_', '').replace('#', '')
                # Köşeli parantezleri temizle [Resim] vb.
                clean_text = re.sub(r'\[.*?\]', '', clean_text)
                
                print(f"📝 Okunacak Metin: {clean_text[:50]}...")
                return clean_text
            else:
                return None

        except Exception as e:
            print(f"❌ Görsel okuma hatası: {e}")
            return None