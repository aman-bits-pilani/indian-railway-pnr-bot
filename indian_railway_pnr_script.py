from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def fetch_pnr_status(pnr):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Comment this if you want to see the browser
    driver = webdriver.Chrome(options=options)

    try:
        url = f"https://www.confirmtkt.com/pnr-status/{pnr}"
        driver.get(url)
        time.sleep(5)  # wait for JavaScript to load content

        print(f"\nPNR: {pnr}")
        print("Fetching status from Confirmtkt...\n")

        status_blocks = driver.find_elements(By.CSS_SELECTOR, ".p-20.bg-white.rounded-10.mt-30")

        if status_blocks:
            for block in status_blocks:
                print(block.text)
        else:
            print("No status found or still loading. Please check manually.")
    
    finally:
        driver.quit()

# Example usage
fetch_pnr_status("2135012418")
fetch_pnr_status("2663243998")
fetch_pnr_status("2715704719")