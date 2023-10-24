import os
import json
import time
import hashlib
import datetime
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urlencode
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


page = 0
shop_id = '302162413'
user_id = '302181998'
brand_name = '大成貢丸'

service = ChromeService(ChromeDriverManager().install())
req_url_format = f'https://shopee.tw/api/v4/seller_operation/get_shop_ratings?limit=6&offset=page_size&shop_id={shop_id}&user_id={user_id}'

opt = webdriver.ChromeOptions()
opt.add_argument('--no-sandbox')
opt.add_argument('--headless')
opt.add_argument('user-agent=%s' % 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36')
opt.add_argument('--start-maximized')
opt.add_argument('--disable-notifications')
opt.add_argument('--disable-blink-features=AutomationControlled')

html_parser = 'html.parser'
collected_datasets = []
driver = webdriver.Chrome(service=service, options=opt)

while True:
    req_url = req_url_format.replace('page_size', str(page))
    driver.get(req_url)
    time.sleep(10)

    print('Sleeping 5 seconds...')
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, html_parser)
    comment_api_json_str = soup.select_one('pre').text

    if 'code' not in list(json.loads(comment_api_json_str).keys()):
        break

    page += 6

    collected_datasets.append(comment_api_json_str)

driver.close()

print('Parsing page source contents is started.')

date_format = '%Y-%m-%d'
keyword_path = contents[0][0:-1]

handler = open(keyword_path, 'r')
keywords = handler.readlines()
handler.close()

index = 0
for keyword in keywords:
    keywords[index] = keyword[0:-1]
    index += 1


csv_str = '廠商名稱,評論內容,評論內容hash,貼文來源,出現的關鍵字\n'

for collected_data in collected_datasets:
    json_obj = json.loads(collected_data)

    for data in json_obj['data']:
        if data['comment'] is None:
            continue

        comment = data['comment'].replace('\n', ' ')
        if comment == '':
            continue

        for product_info in data['product_items']:
            plain_text = comment + str(product_info['snapshotid']) + str(product_info['modelid'])
            hashed_comment = hashlib.sha1(plain_text.encode('utf-8')).hexdigest()
            find_keyword = False
            the_keyword = ''
            product_name = product_info['name']
            for keyword in keywords:
                if keyword in product_name:
                    the_keyword = keyword
                    find_keyword = True
                    break

            if find_keyword is False:
                continue

            csv_rec_format = ('%s,' * 5)[0:-1]
            record_str = csv_rec_format % (
                brand_name,
                '"' + comment + '"',
                hashed_comment,
                '蝦皮購物評論',
                the_keyword,
            )
            csv_str += record_str + '\n'


output_path = './shopee_review_once.csv'
handler = open(output_path, 'w')
handler.write(csv_str)
handler.close()


print('The %s file is saved.' % output_path)
print('Crawling is done.')
