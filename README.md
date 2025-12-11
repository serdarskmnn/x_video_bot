# 📱 X (Twitter) to Video Bot

This project is an automation tool that scrapes tweets from X (Twitter) and converts them into engaging vertical videos (Shorts/Reels/TikTok format) by adding background gameplay footage.

## 🚀 Features

* **Safe Scraping:** Uses `Playwright` to mimic a real browser environment, effectively bypassing X's bot detection systems.
* **Dynamic Rendering:** Converts tweet data (Text, Avatar, Username, Media) into high-quality images using custom HTML/CSS templates (`Jinja2`).
* **Text-to-Speech (TTS):** Utilizes Google Text-to-Speech (gTTS) to generate fluent and clear voiceovers for the tweet content.
* **Auto-Editing:**
    * Automatically selects a random video from your background library.
    * Resizes and centers the background video for vertical (9:16) format.
    * Overlays the tweet image perfectly in the center.
    * Synchronizes video duration with the audio length.

## 🛠️ Installation

Clone the repository and install the required dependencies:

```bash
# Clone the repository
git clone [https://github.com/serdarskmnn/x_video_bot.git](https://github.com/serdarskmnn/x_video_bot.git)
cd x_video_bot

# Create a virtual environment (Recommended)
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

⚙️ Configuration
To fetch tweets successfully, the bot requires your X (Twitter) cookies.

Create a file named cookies.json inside the config/ folder.

Log in to X on your browser.

Open Developer Tools (F12) -> Application -> Cookies (or use the "EditThisCookie" extension).

Copy the values and save them in the file using the following format:
{
    "auth_token": "YOUR_AUTH_TOKEN",
    "ct0": "YOUR_CT0_VALUE",
    "guest_id": "OPTIONAL",
    "twid": "OPTIONAL"
}
Note: auth_token and ct0 are mandatory fields.

🎬 Usage
Prepare Backgrounds: Place your gameplay or satisfying videos (.mp4) into the assets/background/ folder. The system will pick one randomly.

Run the Bot: python3 main.py

Enter ID: Paste the Tweet ID when prompted in the terminal.

Done: The generated video will be saved in the output/ directory.

📂 Project Structure
x_video_bot/
├── assets/
│   ├── background/    # Place background videos here
│   ├── templates/     # HTML/CSS templates for rendering
│   └── temp/          # Temporary files (Auto-cleaned)
├── config/
│   └── cookies.json   # Auth cookies (Not included in repo)
├── modules/
│   ├── scraper.py     # Data fetching via Playwright
│   ├── renderer.py    # HTML to Image converter
│   ├── audio_gen.py   # TTS module (Google)
│   └── video_editor.py# Video assembly and editing
├── output/            # Final rendered videos
├── main.py            # Entry point
└── requirements.txt


⚠️ Disclaimer
This project is developed for educational and hobby purposes only. The user is solely responsible for any use that may violate X (Twitter) Terms of Service.

👨‍💻 Developer
Serdar - https://github.com/serdarskmnn

