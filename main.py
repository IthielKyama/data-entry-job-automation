from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from dotenv import load_dotenv

load_dotenv()

FORM_LINK = os.environ.get("FORM_LINK")

response = requests.get("https://appbrewery.github.io/Zillow-Clone/")
webpage = response.text
soup = BeautifulSoup(webpage, "html.parser")

all_links = soup.find_all(class_="StyledPropertyCardDataArea-anchor")
link_list = [item.get("href") for item in all_links]

prices = soup.find_all(class_="PropertyCardWrapper__StyledPriceLine")
price_list = [item.getText().replace("/mo", "").split("+")[0] for item in prices]

addresses = soup.find_all(name="address")
address_list = [item.getText().strip() for item in addresses]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(FORM_LINK)

time.sleep(3)

for num in range(3):
    address_field = driver.find_element(By.XPATH,
                                        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_field.send_keys(address_list[num])
    price_field = driver.find_element(By.XPATH,
                                      '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_field.send_keys(price_list[num])
    link_field = driver.find_element(By.XPATH,
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_field.send_keys(link_list[num])
    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    submit.click()

    time.sleep(2)
    submit_again = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    submit_again.click()
    time.sleep(2)
