from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

# Setări Chrome
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Pornește WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Deschide pagina comunității
community_url = "    "  # <- înlocuiește cu linkul tău real
driver.get(community_url)

# Așteaptă logarea dacă e nevoie
input("Loghează-te dacă e nevoie, apoi apasă Enter...")

usernames = set()
scroll_pause = 3
same_count = 0
max_same_scrolls = 5

last_count = 0

while True:
    # Adună articolele vizibile
    articles = driver.find_elements(By.TAG_NAME, "article")

    for article in articles:
        try:
            spans = article.find_elements(By.TAG_NAME, "span")
            for span in spans:
                text = span.text.strip()
                if text.startswith("@") and len(text) > 1 and " " not in text:
                    usernames.add(text)

        except:
            continue

    # Scroll jos
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(scroll_pause)

    # Verifică dacă mai aduce ceva nou
    current_count = len(usernames)
    print(f"Utilizatori unici: {current_count}")

    if current_count == last_count:
        same_count += 1
    else:
        same_count = 0
        last_count = current_count

    if same_count >= max_same_scrolls:
        print("\n[✓] Nu se mai încarcă utilizatori noi. Oprire automată.")
        break

# Salvează rezultatele
with open("users10.txt", "w", encoding="utf-8") as f:
    for user in sorted(usernames):
        f.write(f"{user} | https://twitter.com/{user[1:]}\n")

print(f"[✓] Gata! {len(usernames)} utilizatori salvați în users.txt")

# Așteaptă înainte de închidere
input("Apasă Enter pentru a închide browserul...")
driver.quit()
