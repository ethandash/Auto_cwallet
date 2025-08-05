# auto_cwallet.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

# Ambil dari environment
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
        print("🔧 Membuka Cwallet...")
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

        # Cari tombol "Daily Reward" atau "Check-in"
        try:
            reward_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Daily')]")
            reward_btn.click()
            time.sleep(3)
            result = driver.find_element(By.CLASS_NAME, "reward-amount").text
            print(f"🎉 Berhasil claim: {result}")
            return f"✅ Claim berhasil: {result}"
        except:
            # Cek apakah sudah claim hari ini
            try:
                if "already" in driver.page_source.lower():
                    print("⏳ Sudah claim hari ini")
                    return "Sudah claim hari ini"
            except:
                pass
            return "❌ Tidak bisa claim (tidak ada tombol)"

    except Exception as e:
        print(f"❌ Error: {e}")
        return f"Gagal: {str(e)}"
    finally:
        driver.quit()

if __name__ == "__main__":
    result = claim_cwallet()
    print(result)

def send_telegram(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    if not token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": f"💰 Cwallet Daily Claim\n{message}"}
    try:
        import requests
        requests.post(url, data=data)
    except:
        pass

# Di akhir
if __name__ == "__main__":
    result = claim_cwallet()
    send_telegram(result)
