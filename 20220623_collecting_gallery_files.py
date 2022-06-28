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
from selenium.webdriver.common.alert import Alert #import cv2
from selenium.webdriver.common.keys import Keys
from urllib.request import urlretrieve
# -----------------------------------------------------------------------------------------------
# 웹 서칭 함수
def go_web(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(
        '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"')
    driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=chrome_options)
    driver.get(url)
    time.sleep(2)
    return driver
# -----------------------------------------------------------------------------------------------
# 2.
save_base_dir = r'C:\Users\dream\OneDrive\바탕 화면\pixar_sing_general_type'
if not os.path.exists(save_base_dir): os.mkdir(save_base_dir)

# -----------------------------------------------------------------------------------------------
# 3. ash 'Gunter','Warthogs','Whale',
#
characters = ["Angie's daughter","Meena's grandfather","Meena's grandmother","Meena's mother","Rosita & Norman's children"]
characters = ['Sherry-Anne']
characters = ['Angie','Ash','Buster Moon','Clay Calloway','Gunter','Jimmy Crystal','Johnny','Meena','Mike','Nooshy','Porsha Crystal','Rosita','Alfonso','Judith','Klaus Kickenklober',
              'Lance','Miss Crawly','Nana Noodleman','Nancy','Norman','The Q-Teez','Richard','Becky','Big Daddy','Darius','Eddie',
              'Baboon','Beaver','Bob','Bull','Bull Prince and Cow Princess','Bunnies','Chimps and Turtle',
              'Crocodile','Daniel','Derek','Ducklings','Flamingos','Gorilla robbers','Harry','Herman','Hippo', 'Hippo and Rabbits','Hobbs','Horse','Jerry','Karen','Kip Casey','Llama','Linda Le Bon','Mario','Mason',
              'Sheep','Shrimp','Slug','Snake','Spiders','Steve','Tarsier','Turtles']
characters = sorted(characters)

# -------------------------------------------------------------------------------------------------------
# 4.
#pixar_sing_characters = ['sing2 ' + c.lower() for c in characters]
#pixar_sing_characters = sorted(pixar_sing_characters)

# ---------------------------------------------------------------------------------------------
sleep_time = 3
base_url = 'https://sing.fandom.com/'
# -------------------------------------------------------------------------------------------------------
# 5.
main_images = []
for character in characters :
    character_save_name = '_'.join(character.split(' ')).lower()
    print(character_save_name)
    character_save_dir = os.path.join(save_base_dir, character_save_name)
    if not os.path.exists(character_save_dir):
        os.mkdir(character_save_dir)
        # ------------------------------------------------------------
        gallery_url = base_url + character + '/Gallery'
        print(gallery_url)
        driver = go_web(gallery_url)
        time.sleep(3)
        new_img_dirs = []
        images = driver.find_elements_by_css_selector('a > img')
        k = 0

        #print('%s 케릭터 검색 시 %d 개의 이미지가 찾아짐'%(character,len(images)))
        for image in images :
            alt_text = image.get_attribute('alt').lower()
            image_url = image.get_attribute('src')
            if 'wiki' not in alt_text :
                if alt_text :
                    if 'png' in image_url :
                        k += 1
                        img_save_dir = os.path.join(character_save_dir, character_save_name + '_' + str(k) + '.png')
                        image_save_url = image_url.split('png')[0] + 'png'
                        urllib.request.urlretrieve(image_save_url, img_save_dir)
        print()
        print()
        driver.quit()

    """
    # ---------------------------------------------------------------------------------------------------
    # 1. main image 얻기
    #main_[0].get_attribute('src').split('png')[0]
    #main_image_url = main_image + 'png'

    #pure_name = '_'.join(character.split(' ')).lower() +'.png'
    #save_name = os.path.join(save_base_dir,pure_name)
    #print(main_image_url)
    #print(save_name)
    #urllib.request.urlretrieve(main_image_url, save_name)
    # ---------------------------------------------------------------------------------------------------
    # 2. 동물 이름 얻기
    #driver.quit()
#print(main_images)
"""