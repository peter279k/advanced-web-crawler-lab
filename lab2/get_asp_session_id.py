import re
import requests


headers = {
    'Cookie': 'CSRFToken=any_token',
    'CSRFToken': 'any_token',
}
response = requests.get('https://ezpost.post.gov.tw/api/staticData/keyValue/MDX01', headers=headers)
resp_headers = response.headers
set_cookie_str = resp_headers['Set-Cookie']

matched = re.findall(r'ASP.NET_SessionId=(\w+)', set_cookie_str)
if len(matched) != 1:
    print('Cannot find the Set-Cookie response header value!')
    exit(1)


asp_net_session = matched[0]
print('The ASP.NET Session is: %s' % asp_net_session)
