import asyncio
import json
import os
from playwright.async_api import async_playwright

COOKIES_PATH = os.path.join('config', 'cookies.json')

class TweetScraper:
    async def get_thread(self, tweet_id):
        print(f"🔄 Tweet Çekiliyor... ID: {tweet_id}")
        
        async with async_playwright() as p:
            # Tarayıcıyı başlat
            browser = await p.chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled'])
            context = await browser.new_context(viewport={'width': 1366, 'height': 768})
            
            # Çerezleri yükle
            if os.path.exists(COOKIES_PATH):
                with open(COOKIES_PATH, 'r') as f:
                    cookies = json.load(f)
                clist = [{'name': k, 'value': v, 'domain': '.x.com', 'path': '/'} for k, v in cookies.items() if v]
                await context.add_cookies(clist)
            
            page = await context.new_page()
            try:
                # Tweet sayfasına git
                await page.goto(f"https://x.com/i/web/status/{tweet_id}", timeout=60000, wait_until='domcontentloaded')
                await page.wait_for_selector('[data-testid="tweetText"]', timeout=20000)
                await asyncio.sleep(2) # İçeriğin tam oturması için bekle
            except Exception as e:
                print(f"❌ Sayfa yükleme hatası: {e}")
                await browser.close()
                return []

            # Veriyi DOM'dan çek
            tweet_data = await page.evaluate('''() => {
                const article = document.querySelector('article');
                if (!article) return null;
                const textEl = article.querySelector('[data-testid="tweetText"]');
                const userEl = article.querySelector('[data-testid="User-Name"]');
                
                // Resim veya Video önizlemesini bul
                let imgEl = article.querySelector('[data-testid="tweetPhoto"] img');
                if (!imgEl) imgEl = article.querySelector('[data-testid="videoPlayer"] video'); 
                
                const avatarEl = article.querySelector('div[data-testid="Tweet-User-Avatar"] img');
                
                let userName = "", userHandle = "";
                if (userEl) {
                    const parts = userEl.innerText.split('\\n');
                    userName = parts[0];
                    userHandle = parts.find(p => p.startsWith('@')) || parts[1] || "";
                }
                return {
                    text: textEl ? textEl.innerText : "",
                    user_name: userName,
                    user_handle: userHandle,
                    user_avatar: avatarEl ? avatarEl.src : null,
                    image_url: imgEl ? (imgEl.src || imgEl.poster) : null,
                    created_at: new Date().toISOString()
                };
            }''')
            
            await browser.close()
            
            if tweet_data:
                tweet_data['id'] = tweet_id
                if tweet_data['user_avatar']: 
                    tweet_data['user_avatar'] = tweet_data['user_avatar'].replace('_normal', '')
                return [tweet_data]
            return []