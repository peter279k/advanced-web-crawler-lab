import time
from DrissionPage import ChromiumPage


p = ChromiumPage()

p.get('https://dcard.tw')
i = p.get_frame('@src^https://challenges.cloudflare.com/cdn-cgi')
if i:
    i('.mark').click()
    time.sleep(15)


print(p.html)
p.stop_loading()
p.quit()
