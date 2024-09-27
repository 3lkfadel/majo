from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import os
import time

options = Options()
# options.add_argument("--headless")
options.headless = True

script_dir = os.path.dirname(_file_)
geckodriver_path = os.path.join(script_dir, 'geckodriver.exe')
service = Service(executable_path=geckodriver_path)

print('Execution started')
driver = webdriver.Firefox(service=service, options=options)
url = 'https://www.alibaba.com/Business-Services_p28?spm=a2700.product_home_newuser.category_overview.category-28'
driver.get(url)

def scrape_page():
    product_elements = driver.find_elements(By.CSS_SELECTOR, 'div.hugo4-pc-grid-item')
    for product in product_elements:
        image_elements = product.find_elements(By.CSS_SELECTOR, 'div.hugo4-product-picture img.picture-image')
        for img in image_elements:
            img_src = img.get_attribute('src')
            print(f'Image URL: {img_src}')

def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

scroll_to_bottom()
scrape_page()

driver.quit()