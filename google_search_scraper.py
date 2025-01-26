from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up options for Chrome to use a custom user-agent to avoid detection
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Set up the WebDriver with options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def google_search(query):
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    # Use WebDriverWait to wait for the results to appear
    try:
        # Wait for the results to be visible
        results_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".tF2Cxc"))
        )
    except Exception as e:
        print(f"ERROR: Couldn't load search results: {e}")
        return []

    results = driver.find_elements(By.CSS_SELECTOR, ".tF2Cxc")  # Select result blocks
    search_results = []

    for result in results:
        try:
            title = result.find_element(By.TAG_NAME, "h3").text
            link = result.find_element(By.CSS_SELECTOR, ".yuRUbf a").get_attribute("href")
            description = result.find_element(By.CSS_SELECTOR, ".IsZvec").text
            search_results.append({"title": title, "link": link, "description": description})
        except Exception as e:
            print(f"Skipping a result due to error: {e}")

    return search_results

# Example usage
query = "Python programming"
results = google_search(query)

if results:
    print(f"Top search results for '{query}':")
    for idx, result in enumerate(results, start=1):
        print(f"\nResult {idx}:")
        print(f"Title: {result['title']}")
        print(f"Link: {result['link']}")
        print(f"Description: {result['description']}")
else:
    print(f"No results found for '{query}'")

driver.quit()
