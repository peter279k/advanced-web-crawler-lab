import os
import csv
import json
import time
import hashlib
import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from seleniumwire import webdriver
from urllib.parse import urlencode
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


brand_infos = []
query_text = '阿中丸子企業總部(振鈁有限公司)'
brand_name = '阿中丸子'
brand_infos.append({'query_text': query_text, 'brand_name': brand_name})


csv_str = '廠商名稱,評論內容,評論內容hash,貼文來源,出現的關鍵字\n'
for brand_info in brand_infos:
    query_text = urlencode(query={'q': brand_info['query_text']})
    brand_name = brand_info['brand_name']
    req_url = f'https://www.google.com/search?{query_text}'
    service = ChromeService(ChromeDriverManager(driver_version='114.0.5735.90').install())

    opt = webdriver.ChromeOptions()
    opt.add_argument('--no-sandbox')
    opt.add_argument('--headless')
    opt.add_argument('user-agent=%s' % 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36')
    opt.add_argument('--start-maximized')
    opt.add_argument('--disable-notifications')
    opt.add_argument('--disable-blink-features=AutomationControlled')

    html_parser = 'html.parser'
    review_dialog_keyword = 'reviewDialog?'
    review_sort = 'reviewSort?'
    driver = webdriver.Chrome(service=service, options=opt)


    driver.get(req_url)
    time.sleep(10)

    print('Sleeping 5 seconds...')
    time.sleep(5)

    print('Open Review dialog...')
    driver.find_element(By.CSS_SELECTOR, 'a[data-async-trigger="reviewDialog"]').click()

    print('Waiting for dialog to be open...')
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, html_parser)
    review_message = soup.select_one('a[data-async-trigger="reviewDialog"]').text
    review_arr = review_message.split(' ')
    review_counter = int(int(review_arr[0].replace(',', '')) / 10)
    counter = 0
    max_counter = 5

    while counter < review_counter:
        if counter > max_counter:
            break

        print('Scrolling the review dialog...')
        element = driver.find_element(By.CSS_SELECTOR, 'div[class="loris"]')
        driver.execute_script("arguments[0].scrollIntoView(true);", element)

        time.sleep(5)
        counter += 1


    page_source = driver.page_source
    driver.close()


    print('Parsing page source contents is started. (%s)' % brand_name)

    date_format = '%Y-%m-%d'
    keyword_path = contents[0][0:-1]

    handler = open(keyword_path, 'r')
    keywords = handler.readlines()
    handler.close()

    index = 0
    for keyword in keywords:
        keywords[index] = keyword[0:-1]
        index += 1


    soup = BeautifulSoup(page_source, html_parser)
    review_messages = soup.select('span[tabindex="-1"]')
    index = 0

    for review_message in review_messages:
        find_keyword = False
        the_keyword = ''
        for keyword in keywords:
            if keyword in review_message.text:
                find_keyword = True
                the_keyword = keyword
                break

        if find_keyword is False or index % 2 == 0:
            index += 1
            continue

        csv_rec_format = ('%s,' * 5)[0:-1]
        record_str = csv_rec_format % (
            brand_name,
            '"' + review_message.text + '"',
            hashlib.sha1(review_message.text.encode('utf-8')).hexdigest(),
            'Google評論',
            the_keyword,
        )
        csv_str += record_str + '\n'

        index += 1


data_path = './data'
if os.path.isdir(data_path) is False:
    os.mkdir(data_path)


output_path = './data/data_%s.csv' % (datetime.datetime.now().strftime(date_format))
handler = open(output_path, 'w')
handler.write(csv_str)
handler.close()


print('The %s file is saved.' % output_path)
print('Crawling is done.')
