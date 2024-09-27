import selenium.webdriver as webdriver
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import time

#         driver.quit()
def scrape_website(website):
    print("Launch chrome browser...")

    chrome_driver_path = "./chromedriver.exe"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        print("Page loaded.")
        html = driver.page_source
        # Check for CAPTCHA elements here and handle accordingly
        # This is a placeholder for your CAPTCHA detection logic
        if "captcha" in html.lower():  # Simple check; adjust according to your needs
            raise Exception("CAPTCHA detected, scraping might be blocked.")
        
        time.sleep(10)
        return html
    except (WebDriverException, TimeoutException) as e:
        print(f"Error occurred while trying to scrape the website: {e}")
        return None
    except Exception as e:
        print(f"CAPTCHA or other exception occurred: {e}")
        return None
    finally:
        driver.quit()

# Extract only relevant textual tags to pass to LLM
def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
