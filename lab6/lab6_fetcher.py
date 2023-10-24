import os
import csv
import time
import datetime
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urlencode
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


vendors = []
shop_name = 'foodji'
brand_name = '新宇禎福記摃丸'
vendors.append({'shop_name': shop_name, 'brand_name': brand_name})


csv_str = '廠商名稱,產品名稱,售價,優惠價格,優惠開始日期,優惠結束日期,搜尋日期,資料來源,產品網址\n'
for vendor in vendors:
    page = 1
    service = ChromeService(ChromeDriverManager().install())
    req_url_format = 'https://www.rakuten.com.tw/shop/shop_name/search/query_text/?p=page_size'
    req_url_format = req_url_format.replace('shop_name', vendor['shop_name'])
    req_url_format = req_url_format.replace('query_text', urlencode(query={'': vendor['brand_name']})[1:])

    opt = webdriver.ChromeOptions()
    opt.add_argument('--no-sandbox')
    opt.add_argument('--headless')
    opt.add_argument('--disable-notifications')

    html_parser = 'html.parser'
    collected_datasets = []
    driver = webdriver.Chrome(service=service, options=opt)
    original_url = req_url_format.split('?')[0]


    while True:
        req_url = req_url_format.replace('page_size', str(page))
        driver.get(req_url)

        print('Sleeping 5 seconds...')
        time.sleep(5)


        if original_url == driver.current_url and page > 1:
            break


        page += 1

        collected_datasets.append(driver.page_source)


    driver.close()

    print('Parsing page source contents is started (%s).' % vendor['shop_name'])

    date_format = '%Y-%m-%d'
    brand_name = vendor['brand_name']
    keyword_path = contents[0][0:-1]

    handler = open(keyword_path, 'r')
    keywords = handler.readlines()
    handler.close()

    index = 0
    for keyword in keywords:
        keywords[index] = keyword[0:-1]
        index += 1


    host_link = 'https://www.rakuten.com.tw'
    product_class_name_info = 'product-name'
    price_class_name_info = 'b-text-prime'

    for collected_data in collected_datasets:
        soup = BeautifulSoup(collected_data, html_parser)
        product_tables = soup.select('a[class="%s"]' % product_class_name_info)
        price_tables = soup.select('span[class="%s"]' % price_class_name_info)
        product_table_index = 0

        for product_info in product_tables:
            product_link = host_link + product_info['href']
            product_name = product_info.text
            find_keyword = False
            for keyword in keywords:
                if keyword in product_name:
                    find_keyword = True
                    break

            if find_keyword is False:
                continue

            price = price_tables[product_table_index].text.replace(',', '')
            csv_rec_format = ('%s,' * 9)[0:-1]
            record_str = csv_rec_format % (
                brand_name,
                '"' + product_name + '"',
                int(price),
                'N/A',
                'N/A',
                'N/A',
                datetime.datetime.now().strftime(date_format),
                '樂天市場',
                product_link,
            )
            csv_str += record_str + '\n'

            product_table_index += 1

        page += 1


data_path = './data'
if os.path.isdir(data_path) is False:
    os.mkdir(data_path)


output_path = './data/data_%s.csv' % (datetime.datetime.now().strftime(date_format))
handler = open(output_path, 'w')
handler.write(csv_str)
handler.close()


print('The %s file is saved.' % output_path)
print('Crawling is done.')
