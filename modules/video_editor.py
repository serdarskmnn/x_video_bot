import os
import random
from moviepy.editor import VideoFileClip, ImageClip, AudioFileClip, CompositeVideoClip

class VideoEditor:
    def __init__(self, bg_folder_path):
        self.bg_folder_path = bg_folder_path

    def _get_random_background(self):
        """Klasörden rastgele video seçer."""
        try:
            files = [f for f in os.listdir(self.bg_folder_path) if f.lower().endswith(('.mp4', '.mov', '.mkv'))]
            if not files: return None
            return os.path.join(self.bg_folder_path, random.choice(files))
        except: return None

    def create_video(self, image_path, audio_path, output_path):
        print("🎬 Video montajı başlıyor...")
        
        try:
            audio = AudioFileClip(audio_path)
        except: 
            print("❌ Ses dosyası hatası")
            return None

        bg_video_path = self._get_random_background()
        if not bg_video_path:
            print("❌ Arka plan videosu bulunamadı!")
            return None

        W, H = 1080, 1920

        try:
            # 1. Arka Plan (Oyun Videosu)
            gameplay = VideoFileClip(bg_video_path)
            
            # Loop ve Kesme
            if gameplay.duration < audio.duration:
                gameplay = gameplay.loop(duration=audio.duration)
            
            max_start = max(0, gameplay.duration - audio.duration)
            start = random.uniform(0, max_start)
            gameplay = gameplay.subclip(start, start + audio.duration)
            
            # Tam Ekran Yapma (Center Crop)
            gameplay = gameplay.resize(height=H)
            if gameplay.w < W: gameplay = gameplay.resize(width=W)
            gameplay = gameplay.crop(x1=gameplay.w/2 - W/2, width=W, height=H)
            
            # Sesini kapat
            gameplay = gameplay.without_audio()

            # 2. Tweet Resmi (Ortala)
            tweet_img = ImageClip(image_path).set_duration(audio.duration)
            tweet_img = tweet_img.resize(width=900) # Biraz küçült
            tweet_img = tweet_img.set_position(('center', 'center'))

            # 3. Birleştir
            final = CompositeVideoClip([gameplay, tweet_img]).set_audio(audio)
            
            # 4. Render
            print(f"⚙️ Render yapılıyor... ({output_path})")
            final.write_videofile(
                output_path, fps=30, codec="libx264", audio_codec="aac",
                temp_audiofile="temp-audio.m4a", remove_temp=True,
                preset="ultrafast", threads=4, logger=None
            )
            print("✅ Video hazır!")
            return output_path
        except Exception as e:
            print(f"❌ Render Hatası: {e}")
            return None