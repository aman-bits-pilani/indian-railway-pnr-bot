import asyncio
import os
import time
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from telegram import Bot

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

async def send_to_telegram(message):
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)

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
            full_message = f"📌 Current PNR Status for PNR:{pnr}\n\n"
            for block in status_blocks:
                print(block.text)
                full_message += block.text + "\n\n"
            # Send to Telegram
            asyncio.run(send_to_telegram(full_message))
        else:
            message = f"PNR: {pnr}\nNo status found or still loading."
            print(message)
            asyncio.run(send_to_telegram(message))

    finally:
        driver.quit()

# Example usage
pnrs = ["2135012418", "2663243998", "2715704719"]
for pnr in pnrs:
    fetch_pnr_status(pnr)
