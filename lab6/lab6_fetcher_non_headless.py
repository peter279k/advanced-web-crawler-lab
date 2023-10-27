import os
import csv
import time
import hashlib
import datetime
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


brand_infos = []
brand_infos.append({'page_name': 'achunwanna', 'brand_name': '阿中丸子',})


csv_str = '廠商名稱,貼文摘要,貼文摘要hash,貼文內容,貼文來源\n'
for brand_info in brand_infos:
    page_name = brand_info['page_name']
    brand_name = brand_info['brand_name']
    service = ChromeService(ChromeDriverManager().install())
    req_url_format = 'https://www.facebook.com/%s'


    opt = webdriver.ChromeOptions()
    opt.add_argument('--no-sandbox')
    opt.add_argument('--disable-gpu')
    opt.add_argument('--disable-notifications')

    html_parser = 'html.parser'
    driver = webdriver.Chrome(service=service, options=opt)

    req_url = req_url_format % page_name
    driver.get(req_url)

    print('Sleeping 5 seconds...')
    time.sleep(5)

    driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Close"]').click()
    time.sleep(5)

    for count in list(range(1, 6)):
        print('Scrolling No.%s times' % count)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(5)


    collected_data = driver.page_source
    driver.close()

    print('Parsing page source contents is started.')


    date_format = '%Y-%m-%d'

    soup = BeautifulSoup(collected_data, html_parser)
    post_tables = soup.select('div[data-ad-comet-preview="message"]')

    for post_table in post_tables:
        single_post = post_table.select('div[style="text-align: start;"]')
        single_post_contents = ''
        for single_post_sentence in single_post:
            single_post_contents += single_post_sentence.text


        single_post_contents = single_post_contents.replace('\n', ' ')
        record_str = '%s,"%s",%s,"%s",Facebook\n' % (
            brand_name,
            single_post_contents.replace('\n', '').replace(',', ' '),
            hashlib.sha1(single_post_contents.encode('utf-8')).hexdigest(),
            single_post_contents.replace('\n', '').replace(',', ' '),
        )
        csv_str += record_str


data_path = './data'
if os.path.isdir(data_path) is False:
    os.mkdir(data_path)


output_path = './data/data_%s.csv' % (datetime.datetime.now().strftime(date_format))
handler = open(output_path, 'w')
handler.write(csv_str)
handler.close()


print('The %s file is saved.' % output_path)
print('Crawling is done.')
