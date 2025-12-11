import asyncio
import os
from modules.scraper import TweetScraper
from modules.renderer import TweetRenderer
from modules.audio_gen import AudioGenerator
from modules.video_editor import VideoEditor

# --- AYARLAR ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
TEMP_DIR = os.path.join(ASSETS_DIR, 'temp')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
BG_VIDEO_FOLDER = os.path.join(ASSETS_DIR, 'background')

# Klasörleri oluştur
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(BG_VIDEO_FOLDER, exist_ok=True)

async def main():
    print("🚀 X Video Bot (Lite Sürüm) Başlatılıyor...")

    tweet_id = input("📌 Tweet ID: ").strip()
    if not tweet_id: 
        print("❌ ID girmediniz.")
        return

    # Modülleri Başlat
    scraper = TweetScraper()
    renderer = TweetRenderer()
    audio_gen = AudioGenerator()
    video_editor = VideoEditor(bg_folder_path=BG_VIDEO_FOLDER)
    
    # 1. VERİ ÇEK
    tweets = await scraper.get_thread(tweet_id)
    if not tweets: return
    tweet = tweets[0]
    
    print(f"📋 İşlenen Tweet: {tweet['text'][:30]}...")

    # 2. GÖRSEL OLUŞTUR
    image_path = await renderer.render_tweet(tweet)
    if not image_path: return

    # 3. SES OLUŞTUR (SADECE TWEET METNİ)
    print("🧹 Seslendiriliyor...")
    
    # Metin temizliği (Yeni satırları noktaya çevir ki robot nefes alsın)
    clean_text = tweet['text'].replace("\n", ". ").replace("http", " link ")
    
    # Dosya yolu
    audio_path = os.path.join(TEMP_DIR, f"audio_{tweet['id']}.mp3")
    
    if not await audio_gen.generate_audio(clean_text, audio_path): return

    # 4. VİDEO OLUŞTUR
    final_output = os.path.join(OUTPUT_DIR, f"final_{tweet['id']}.mp4")
    
    # Background klasör kontrolü
    if not os.path.exists(BG_VIDEO_FOLDER) or not os.listdir(BG_VIDEO_FOLDER):
        print("⚠️ HATA: 'assets/background' klasörüne video atın!")
        return

    if video_editor.create_video(image_path, audio_path, final_output):
        print(f"\n✨✨ VİDEO BİTTİ: {final_output} ✨✨")

if __name__ == "__main__":
    asyncio.run(main())