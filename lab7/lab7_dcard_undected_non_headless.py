import time
import requests
from DrissionPage import SessionPage
import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

p = SessionPage()
p.get('https://nowsecure.nl')
i = p.get_frame('@src^https://challenges.cloudflare.com/cdn-cgi')
if i:
    i('.mark').click()


print(p.response.text)
p.close()
