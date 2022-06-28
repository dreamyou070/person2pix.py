import os
from PIL import Image
import time
import bs4
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import urllib.request
import requests
from selenium.webdriver.common.keys import Keys
import time
import json
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 웹 서칭 함수
def go_web(url) :
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"')
    driver = webdriver.Chrome(executable_path = "chromedriver.exe", chrome_options=chrome_options)
    driver.get(url)
    time.sleep(2)
    return driver

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 웹 서칭 함수

base_dir = r'C:\Users\dream\OneDrive\바탕 화면\google'
if not os.path.exists(base_dir): os.mkdir(base_dir)

characters = ['piglet']
cs = ['pixar sing ' + c.lower() for c in characters]
characters = sorted(cs)
sleep_time = 3
url = 'https://www.google.com/?&bih=1038&biw=2048&hl=ko'
for character in characters:
    character = character.lower()
    # ----------------------------------------------------------------------------------
    character_dir = os.path.join(base_dir, '_'.join(character.split(' ')[2:]))
    if not os.path.exists(character_dir): os.mkdir(character_dir)
    # ----------------------------------------------------------------------------------
    driver = go_web(url)

    query_box = driver.find_elements_by_css_selector("div>div>div>input")[0]
    query_box.send_keys(character)
    ok_button = driver.find_elements_by_css_selector("div>div>center>input")[0]
    driver.find_elements_by_css_selector("div>div>center>input")[2].click()
    time.sleep(sleep_time)
    # ----------------------------------------------------------------------------------
    driver.find_elements_by_xpath('//*[@id="hdtb-msb"]/div[1]/div/div[2]/a')[0].click()
    time.sleep(sleep_time)
    # ----------------------------------------------------------------------------------.


    while True:
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)
        check = driver.find_elements_by_xpath('//*[@id="ZCHFDb"]/div/div/span[2]')[0].text
        if check.startswith('대한민국'):
            break

    images = driver.find_elements_by_css_selector("div>a>div>img")
    print(len(images))
    for n, image in enumerate(images, 1):
        image_url = image.get_attribute('src')
        pure_name = '_'.join(character.split(' ')[2:]) + '_' + str(n) + '.jpg'
        image_dir = os.path.join(character_dir, pure_name)
        try :
            urllib.request.urlretrieve(image_url, image_dir)
        except :
            continue
    driver.quit()