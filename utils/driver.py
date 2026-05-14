from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import platform

def get_driver(headless=False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    # Use system chromedriver in CI, webdriver-manager locally
    if os.environ.get("CI"):
        driver = webdriver.Chrome(options=options)
    else:
        os.environ["WDM_ARCH"] = "arm64"
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    driver.implicitly_wait(5)
    return driver
