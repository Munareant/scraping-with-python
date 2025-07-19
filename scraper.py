from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=chrome_options)

community_url = "https://x.com/i/communities/1672458762852921344"  # <- LINK
driver.get(community_url)

input("Please log in and wait for the page to load...")

usernames = set()
scroll_pause = 3
same_count = 0
max_same_scrolls = 5

last_count = 0

while True:
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

    if len(usernames) >= 15:
        print("\n I found 15 usernames, stopping the script.")
        break

    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(scroll_pause)

    current_count = len(usernames)
    print(f"Username: {current_count}")

    if current_count == last_count:
        same_count += 1
    else:
        same_count = 0
        last_count = current_count

    if same_count >= max_same_scrolls:
        print("\n There's no new usernames, stopping the script.")
        break

with open("users.txt", "w", encoding="utf-8") as f:
    for user in sorted(usernames):
        f.write(f"{user} | https://twitter.com/{user[1:]}\n")

print(f" Done! {len(usernames)} usernames were saved in users.txt")

input("Press the enter key to exit...")
driver.quit()
