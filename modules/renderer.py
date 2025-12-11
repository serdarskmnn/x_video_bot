import os
from jinja2 import Environment, FileSystemLoader
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'assets', 'templates')
OUTPUT_DIR = os.path.join(BASE_DIR, 'assets', 'temp')
os.makedirs(OUTPUT_DIR, exist_ok=True)

class TweetRenderer:
    def __init__(self):
        # Şablon dosyasını yükle
        self.env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
        self.template = self.env.get_template('tweet_card.html')

    async def render_tweet(self, tweet_data):
        tweet_id = tweet_data.get('id')
        print(f"🎨 Tweet görselleştiriliyor...")

        # HTML içeriğini doldur
        html_content = self.template.render(
            user_name=tweet_data.get('user_name'),
            user_handle=tweet_data.get('user_handle'),
            user_avatar=tweet_data.get('user_avatar'),
            text=tweet_data.get('text'),
            image_url=tweet_data.get('image_url'),
            created_at=tweet_data.get('created_at', '')[:10]
        )

        # Fotoğrafını çek
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(device_scale_factor=2)
            await page.set_content(html_content)
            
            card_element = await page.query_selector('#tweet-card')
            
            output_path = None
            if card_element:
                output_path = os.path.join(OUTPUT_DIR, f"tweet_{tweet_id}.png")
                await card_element.screenshot(path=output_path)
                print(f"✅ Görsel kaydedildi: {output_path}")
            
            await browser.close()
            return output_path