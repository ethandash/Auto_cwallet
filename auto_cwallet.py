# auto_cwallet.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

EMAIL = os.getenv("CWALLET_EMAIL")
PASSWORD = os.getenv("CWALLET_PASS")

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=options)

def claim_cwallet():
    driver = get_driver()
    try:
        driver.get("https://cwallet.com")
        time.sleep(5)

        # Login
        driver.find_element(By.NAME, "email").send_keys(EMAIL)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Log In')]").click()
        time.sleep(5)

        if "dashboard" not in driver.current_url:
            print("❌ Login gagal")
            return "Login gagal"

        # Coba klik tombol hadiah harian
        try:
            driver.find_element(By.XPATH, "//button[contains(text(), 'Daily')]").click()
            time.sleep(3)
            result = driver.find_element(By.CLASS_NAME, "reward-amount").text
            print(f"🎉 Berhasil claim: {result}")
            return f"✅ Berhasil: {result}"
        except:
            return "⏳ Sudah claim hari ini"
    except Exception as e:
        return f"❌ Gagal: {str(e)}"
    finally:
        driver.quit()

def send_telegram(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    if not token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": f"💰 Cwallet Auto-Claim\n{message}"}
    try:
        import requests
        requests.post(url, data=data)
    except:
        pass

if __name__ == "__main__":
    result = claim_cwallet()
    send_telegram(result)
