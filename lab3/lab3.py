import os
import csv
import time
import random
import datetime
import requests
from bs4 import BeautifulSoup
import undetected_chromedriver as webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


vendor_csv = './vendor.csv'
if os.path.isfile(vendor_csv) is False:
    print('The %s file is not found.' % vendor_csv)
    exit(1)

with open(vendor_csv, 'r') as f:
    vendor_contents = f.readlines()

vendors = []
shopee_id = 'achunwanna'
brand_name = '阿中丸子'
vendors.append({'shopee_id': shopee_id, 'brand_name': brand_name})


csv_str = '廠商名稱,產品名稱,售價,優惠價格,優惠開始日期,優惠結束日期,搜尋日期,資料來源,產品網址\n'
for vendor in vendors:
    page = 0
    service = ChromeService(ChromeDriverManager().install())
    req_url_format = 'https://shopee.tw/shopee_id?page=page_size&sortBy=sales'
    req_url_format = req_url_format.replace('shopee_id', vendor['shopee_id'])

    opt = webdriver.ChromeOptions()
    opt.add_argument('--no-sandbox')
    opt.add_argument('--headless')
    opt.add_argument('--disable-notifications')

    html_parser = 'html.parser'
    collected_datasets = []
    driver = webdriver.Chrome(service=service, options=opt)

    while True:
        req_url = req_url_format.replace('page_size', str(page))
        driver.get(req_url)

        print('Sleeping from 60 to 100 seconds...')
        random.seed()
        time.sleep(random.randint(60, 100))

        soup = BeautifulSoup(driver.page_source, html_parser)
        shop_search_table = soup.select_one('div[class="shop-search-result-view"]')

        if shop_search_table is None:
            break

        page += 1

        collected_datasets.append(driver.page_source)


    driver.close()

    print('Parsing page source contents is started (%s).' % vendor['shopee_id'])

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


    host_link = 'https://shopee.tw'
    search_table_class_name = 'shop-search-result-view'
    product_link_class_name = 'link'
    product_name_class_name = 'name'

    for collected_data in collected_datasets:
        soup = BeautifulSoup(collected_data, html_parser)
        shop_search_table = soup.select_one('div[class="%s"]' % search_table_class_name)
        product_infos = shop_search_table.select('a[data-sqe="%s"]' % product_link_class_name)

        for product_info in product_infos:
            product_link = host_link + product_info['href']
            product_name = product_info.select_one('div[data-sqe="%s"] > div > div' % product_name_class_name).text
            find_keyword = False
            for keyword in keywords:
                if keyword in product_name:
                    find_keyword = True
                    break

            if find_keyword is False:
                continue

            price = int(product_info.select('span')[-1].text.replace(',', ''))
            csv_rec_format = ('%s,' * 9)[0:-1]
            record_str = csv_rec_format % (
                brand_name,
                '"' + product_name + '"',
                price,
                'N/A',
                'N/A',
                'N/A',
                datetime.datetime.now().strftime(date_format),
                '蝦皮購物',
                product_link,
            )
            csv_str += record_str + '\n'

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
