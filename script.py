import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURATION ---
CSV_FILE = r"E:\Spotify playlist\hindi moosic.csv"
DOWNLOAD_FOLDER = r"E:\Spotify playlist\hindi moosic"
SKIPPED_FILE = r"E:\Spotify playlist\skipped_songs2.csv"

# --- XPATHS ---
SEARCH_BOX_XPATH = '/html/body/div/div[1]/div[2]/main/div/div/div[2]/div[1]/div/div/div[1]/input'

# Strategy A: Your Specific Path (Targeting the button, not the SVG)
SPECIFIC_DOWNLOAD_XPATH = '/html/body/div/div[1]/div[2]/main/div/div/div[2]/div[3]/div[1]/div[2]/button'

# Strategy B: Generic Backup (Any button with an SVG icon inside the results area)
GENERIC_DOWNLOAD_XPATH = "//div[contains(@class, 'grid')]//button[descendant::svg]"

SETTINGS_BTN_XPATH = '/html/body/div/div[1]/div[2]/header/div/div/div/button'
QUALITY_OPTION_XPATH = '/html/body/div/div[1]/div[2]/header/div/div/div/div/div/section[1]/div/button[2]/div/span[1]'
# -----------------------------

if not os.path.exists(CSV_FILE):
    print(f"Error: Cannot find file at {CSV_FILE}")
    exit()

with open(SKIPPED_FILE, 'w', newline='', encoding='utf-8') as f:
    csv.writer(f).writerow(["Song", "Artist", "Error Reason"])

options = Options()
options.set_preference("browser.download.folderList", 2) 
options.set_preference("browser.download.dir", DOWNLOAD_FOLDER)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "audio/mpeg,audio/flac,audio/wav,application/octet-stream")

print("Opening Firefox...")
driver = webdriver.Firefox(options=options)
driver.get("https://tidal.squid.wtf/")

print("PAUSED FOR 5 SECONDS")
time.sleep(5)

# --- SET QUALITY ---
try:
    print("Setting Quality...")
    wait = WebDriverWait(driver, 5)
    wait.until(EC.element_to_be_clickable((By.XPATH, SETTINGS_BTN_XPATH))).click()
    time.sleep(0.5)
    wait.until(EC.element_to_be_clickable((By.XPATH, QUALITY_OPTION_XPATH))).click()
    time.sleep(0.5)
    driver.find_element(By.XPATH, SETTINGS_BTN_XPATH).click()
    print("Quality set!")
    time.sleep(1)
except Exception as e:
    print(f"WARNING: Could not set quality. ({e})")

# --- MAIN LOOP ---
try:
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        
        for i, row in enumerate(reader):
            if len(row) < 3: continue
            if row[1] == "Song" and row[2] == "Artist": continue

            song_name = row[1]
            artist_name = row[2]
            search_query = f"{song_name} {artist_name}"

            try:
                print(f"[{i}] {search_query[:30]}...", end=" ")

                # 1. FIND & CLEAR
                search_box = driver.find_element(By.XPATH, SEARCH_BOX_XPATH)
                search_box.send_keys(Keys.CONTROL + "a")
                search_box.send_keys(Keys.DELETE)
                search_box.send_keys(search_query)
                search_box.send_keys(Keys.RETURN)
                
                # 2. WAIT FOR BUTTON (Increased to 10s)
                wait = WebDriverWait(driver, 10) # <--- INCREASED AS REQUESTED
                
                download_btn = None
                try:
                    # Try Strategy A (Specific Path)
                    download_btn = wait.until(EC.presence_of_element_located((By.XPATH, SPECIFIC_DOWNLOAD_XPATH)))
                except:
                    # Try Strategy B (Generic Backup) if A fails
                    # This catches cases where the button layout shifts slightly
                    download_btn = wait.until(EC.presence_of_element_located((By.XPATH, GENERIC_DOWNLOAD_XPATH)))
                
                # 3. FORCE CLICK
                driver.execute_script("arguments[0].click();", download_btn)
                print("-> OK")
                
                # Rate Limit Wait
                time.sleep(4)

            except Exception as e:
                error_msg = str(e).split('\n')[0]
                print(f"-> SKIPPED ({error_msg})")
                
                with open(SKIPPED_FILE, 'a', newline='', encoding='utf-8') as skip_f:
                    csv.writer(skip_f).writerow([song_name, artist_name, error_msg])

except KeyboardInterrupt:
    print("\nStopping...")

print("Job Finished.")
driver.quit()