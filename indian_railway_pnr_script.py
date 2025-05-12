import os
import time
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from telegram import Bot

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_to_telegram(message):
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='HTML')

def fetch_pnr_status(pnr):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

    try:
        url = f"https://www.confirmtkt.com/pnr-status/{pnr}"
        driver.get(url)
        time.sleep(5)

        print(f"\nPNR: {pnr}")
        print("Fetching status from Confirmtkt...\n")

        status_blocks = driver.find_elements(By.CSS_SELECTOR, ".p-20.bg-white.rounded-10.mt-30")

        if status_blocks:
            full_message = f"<b>📌 Current PNR Status for PNR: {pnr}</b>\n\n"
            for block in status_blocks:
                print(block.text)
                full_message += block.text + "\n\n"
            send_to_telegram(full_message)
        else:
            message = f"PNR: {pnr}\n❌ No status found or still loading."
            print(message)
            send_to_telegram(message)

    finally:
        driver.quit()

# Example usage
pnrs = ["2135012418", "2715707015", "2663243998", "2715704719"]
for pnr in pnrs:
    fetch_pnr_status(pnr)
