from selenium import webdriver 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep

url = "https://www.pathofexile.com/trade/search/Affliction/9Y3X5BKUK/live"



with webdriver.Chrome() as driver:
    driver.get(url)
    steam_login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,  "/html/body/div[1]/div/div/fieldset[1]/a[1]"))
    )
    steam_login_button.click()
    sleep(5)