from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
from dotenv import load_dotenv
import time


load_dotenv()

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")


def iniciar_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def fazer_login():
    driver = iniciar_driver()
    driver.get("https://app.fixbrokers.com/")
    time.sleep(2)
    driver.find_element(By.NAME, "email").send_keys(USER)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(3)
    return driver
