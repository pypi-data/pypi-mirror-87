from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


def generate_driver(url: str):
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--headless")
    options.add_argument("log-level=3")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    return driver


def description(url: str):
    driver = generate_driver(url)
    description = driver.find_element(By.CLASS_NAME, "tt-video-meta-caption")
    return description.text


# extract_description("https://www.tiktok.com/@foodies/video/6869148881230318853?lang=en")
