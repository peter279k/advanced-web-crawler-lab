import time
import requests
import undetected_chromedriver as webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


service = ChromeService(ChromeDriverManager().install())
req_url = 'https://dcard.tw'


opt = webdriver.ChromeOptions()
opt.add_argument('--no-sandbox')
opt.add_argument('--disable-gpu')
opt.add_argument('--disable-notifications')
opt.add_argument('--auto-open-devtools-for-tabs')
opt.add_argument('User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36')

driver = webdriver.Chrome(service=service, options=opt)

print('Open the new tab to wait Cloudflare detecting...')
driver.execute_script('window.open("https://dcard.tw");')
time.sleep(2)

driver.switch_to.window(window_name=driver.window_handles[0])
print('Sleeping 10 seconds for closing the first tab...')
time.sleep(10)

driver.get('https://google.com')
time.sleep(10)

driver.switch_to.window(window_name=driver.window_handles[0])

driver.save_screenshot('dcard.png')
driver.close()

time.sleep(5)
driver.switch_to.window(window_name=driver.window_handles[0])
driver.close()

print('Capturing the page image is done.')
