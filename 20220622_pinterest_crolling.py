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
import cv2
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
save_base_dir = r'F:\data_type_pixar_sing_pinterest'
if not os.path.exists(save_base_dir): os.mkdir(save_base_dir)

# -----------------------------------------------------------------------------------------------
# 3. ash
characters = ['johnny', 'miss crawly', 'porsha crystal', 'clay calloway', 'gunter','buster moon',
              'noosy','souki','darius','jimmy crystal','rosita','meena','linda le bon','piglet','jerry']
characters = sorted([c.lower() for c in characters])

# -------------------------------------------------------------------------------------------------------
# 4.
pixar_sing_characters = ['sing2 ' + c.lower() for c in characters]
pixar_sing_characters = sorted(pixar_sing_characters)
# ---------------------------------------------------------------------------------------------
sleep_time = 3
url = 'https://www.pinterest.co.kr/'

for character, pixar_sing_character in zip(characters, pixar_sing_characters):

    character_dict_1 = {}
    character_dict_2 = {}
    character_dict_3 = {}
    character_dict_4 = {}

    img_lst1 = []
    img_lst2 = []
    img_lst3 = []
    img_lst4 = []

    print(character)
    print(pixar_sing_character)
    # ----------------------------------------------------------------------------------
    save_character_dir1 = os.path.join(save_base_dir, '_'.join(character.split(' ')) + '_size_1')
    if not os.path.exists(save_character_dir1): os.mkdir(save_character_dir1)
    save_character_dir2 = os.path.join(save_base_dir, '_'.join(character.split(' ')) + '_size_2')
    if not os.path.exists(save_character_dir2): os.mkdir(save_character_dir2)
    save_character_dir3 = os.path.join(save_base_dir, '_'.join(character.split(' ')) + '_size_3')
    if not os.path.exists(save_character_dir3): os.mkdir(save_character_dir3)
    save_character_dir4 = os.path.join(save_base_dir, '_'.join(character.split(' ')) + '_png_type_1')
    if not os.path.exists(save_character_dir4): os.mkdir(save_character_dir4)
    # ----------------------------------------------------------------------------------
    driver = go_web(url)
    driver.find_elements_by_css_selector("div>div>div>div>div>div>div>div>button>div>div")[0].click()
    time.sleep(sleep_time)

    # ---------------------------------------------------------------------------------------------
    # 로그인 하기
    boxes = driver.find_elements_by_tag_name('input')
    boxes[0].send_keys('dreamyou070@naver.com')
    boxes[1].send_keys('qkrtndus1989!')
    driver.find_elements_by_tag_name('button')[7].click()
    print('Login Success...')
    time.sleep(10)
    # ---------------------------------------------------------------------------------------------
    # 쿼리 치기
    query_box = driver.find_elements_by_tag_name('input')[0]
    query_box.send_keys(pixar_sing_character)
    time.sleep(5)
    # 검색어 클릭
    driver.find_elements_by_tag_name('input')[0].click()
    time.sleep(sleep_time)
    driver.find_elements_by_css_selector('#syop_cta > div > div > div > div.Eqh.xuA > div')[0].click()
    time.sleep(sleep_time)

    # ---------------------------------------------------------------------------------------------
    # 크롤 다운
    for i in range(40):
        images = driver.find_elements_by_tag_name('img')
        time.sleep(sleep_time)
        print('%d 번째 페이지에서 %d 개의 이미지 확인됨' % (i + 1, len(images)))
        for image in images:
            try:
                image_names = image.get_attribute('srcset')
                print(image_names)
                image_names = image_names.split('x,')
                if len(image_names) == 4:
                    for n, image_name in enumerate(image_names):

                        if n == 0:
                            image_name = image_name.split(' ')[0]
                            if image_name not in img_lst1:
                                try:
                                    character_dict_1[character] += 1
                                except:
                                    character_dict_1[character] = 1
                                img_lst1.append(image_name)
                                pure_dir = character + '_size_1_' + str(character_dict_1[character]) + '.jpg'
                                save_img_dir = os.path.join(save_character_dir1, pure_dir)
                                urlretrieve(image_name, save_img_dir)
                        if n == 1:
                            image_name = image_name.split(' ')[1]
                            if image_name not in img_lst2:
                                try:
                                    character_dict_2[character] += 1
                                except:
                                    character_dict_2[character] = 1
                                img_lst2.append(image_name)
                                pure_dir = character + '_size_2_' + str(character_dict_2[character]) + '.jpg'
                                save_img_dir = os.path.join(save_character_dir2, pure_dir)
                                urlretrieve(image_name, save_img_dir)
                        if n == 2:
                            image_name = image_name.split(' ')[1]
                            if image_name not in img_lst3:
                                try:
                                    character_dict_3[character] += 1
                                except:
                                    character_dict_3[character] = 1
                                img_lst3.append(image_name)
                                pure_dir = character + '_size_3_' + str(character_dict_3[character]) + '.jpg'
                                save_img_dir = os.path.join(save_character_dir3, pure_dir)
                                urlretrieve(image_name, save_img_dir)
                        if n == 3:
                            image_name = image_name.split(' ')[1]
                            if image_name not in img_lst4:
                                try:
                                    character_dict_4[character] += 1
                                except:
                                    character_dict_4[character] = 1
                                img_lst4.append(image_name)
                                pure_dir = character + '_png_type_1_' + str(character_dict_4[character]) + '.png'
                                save_img_dir = os.path.join(save_character_dir4, pure_dir)
                                urlretrieve(image_name, save_img_dir)
            except:
                continue
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
    driver.quit()