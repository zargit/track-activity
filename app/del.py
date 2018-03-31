from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os
import sys

path = os.path.abspath("./chromedriver")
print(path)

url = "https://edition.cnn.com/"

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(chrome_options=options, executable_path=path)
driver.get(url)
delay = 2 # seconds
try:
    myElem = WebDriverWait(driver, delay)
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")

headlines = driver.find_elements_by_css_selector('.cd__headline-text')

for headline in headlines:
    print(headline.text)

driver.quit()
