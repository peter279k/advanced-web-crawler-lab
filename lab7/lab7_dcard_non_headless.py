import time
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


service = ChromeService(ChromeDriverManager().install())
req_url = 'https://dcard.tw'


opt = webdriver.ChromeOptions()
opt.add_argument('--no-sandbox')
opt.add_argument('--disable-gpu')
opt.add_argument('--disable-notifications')

driver = webdriver.Chrome(service=service, options=opt)

driver.get(req_url)

print('Sleeping 20 seconds...')
time.sleep(20)

driver.save_screenshot("dcard.png")
driver.close()

print('Capturing the page image is done.')
