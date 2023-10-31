import time
from DrissionPage import ChromiumPage, ChromiumOptions


opt = ChromiumOptions()
opt.set_headless(True)
opt.set_argument('--start-maximized')
opt.set_argument('--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36')
p = ChromiumPage(addr_driver_opts=opt)

p.get('https://dcard.tw')
i = p.get_frame('@src^https://challenges.cloudflare.com/cdn-cgi')
if i:
    i('.mark').click()
    time.sleep(15)


print(p.html)
p.stop_loading()
p.quit()
