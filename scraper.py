from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import random
import os

# === CONFIG ===
MAX_PROFILES = 300
CSV_FILENAME = "yc_profiles.csv"
APPEND_TO_CSV = True  # ✅ Set to False to overwrite existing data

# === Helper Function ===
def human_delay(base=2.0, var=1.0):
    time.sleep(base + random.uniform(0, var))

# === Setup Chrome ===
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.startupschool.org/cofounder-matching/candidate/next")

# === Wait for manual login if necessary ===
print("🟡 Waiting 30 seconds in case login is required...")
time.sleep(30)

# === Load existing data if appending ===
if APPEND_TO_CSV and os.path.exists(CSV_FILENAME):
    existing_df = pd.read_csv(CSV_FILENAME)
    existing_names = set(existing_df["Name"].values)
    print(f"📁 Loaded {len(existing_df)} existing profiles from {CSV_FILENAME}")
else:
    existing_df = pd.DataFrame()
    existing_names = set()

profiles_scraped_this_run = []

# === Scraping Loop ===
while len(profiles_scraped_this_run) < MAX_PROFILES:
    try:
        # Wait for profile to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.css-1s8r69b"))
        )

        human_delay(1, 1.2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        human_delay(0.5, 0.5)

        # === Extract Data ===
        name = driver.find_element(By.CSS_SELECTOR, "h1.css-1s8r69b").text

        if name in existing_names:
            print(f"[SKIP] {name} already scraped.")
            skip_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'e1qryfvo1') and contains(text(), 'Skip for now')]")
            skip_btn.click()
            continue

        try:
            linkedin_div = driver.find_element(By.CSS_SELECTOR, "div.css-107cmgv.ekomr440")
            linkedin = linkedin_div.get_attribute("title")
        except:
            linkedin = "N/A"

        profile_texts = driver.find_elements(By.CSS_SELECTOR, "table.css-1ezh3kn td > div.css-1tp1ukf")
        profile_text = "\n".join([p.text for p in profile_texts if p.text.strip()])

        print(f"[{len(profiles_scraped_this_run)+1}] ✅ Scraped: {name}")
        profiles_scraped_this_run.append({
            "Name": name,
            "LinkedIn": linkedin,
            "ProfileText": profile_text
        })

        # Add to known set to prevent rescraping
        existing_names.add(name)

        human_delay(1.5, 1.5)

        # === Click "Skip for now" ===
        skip_btn_found = False
        for _ in range(3):
            try:
                skip_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'e1qryfvo1') and contains(text(), 'Skip for now')]")
                skip_btn.click()
                skip_btn_found = True
                break
            except NoSuchElementException:
                human_delay(1, 0.5)

        if not skip_btn_found:
            print("❌ 'Skip for now' button not found — exiting.")
            break

    except Exception as e:
        print("❌ Error:", e)
        break

# === Final Save ===
if APPEND_TO_CSV and os.path.exists(CSV_FILENAME):
    # Append only the new profiles
    new_df = pd.DataFrame(profiles_scraped_this_run)
    full_df = pd.concat([existing_df, new_df], ignore_index=True)
    full_df.to_csv(CSV_FILENAME, index=False)
else:
    # Overwrite mode or no file yet
    pd.DataFrame(profiles_scraped_this_run).to_csv(CSV_FILENAME, index=False)

print(f"✅ Done. {len(profiles_scraped_this_run)} new profiles saved to {CSV_FILENAME}")
driver.quit()
