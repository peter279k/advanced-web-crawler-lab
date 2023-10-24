import requests


'''
datetime_str = '202310100000'
datetime_str = '202310100600'
datetime_str = '202310110600'
'''

datetime_str = '202310100600'
host_url = 'https://www.cwa.gov.tw/Data/typhoon/TY_NEWS/%s'
req_url = 'https://www.cwa.gov.tw/Data/typhoon/TY_NEWS/PTA_IMGS_%s_zhtw.json' % datetime_str

response = requests.get(req_url)
if response.status_code != 200:
    print(response.status_code)
    exit(1)


resp_json = response.json()
typhoon_name = resp_json['EACH'][0]['id']
print(typhoon_name)

for img_file_name in resp_json['EACH'][0]['list']:
    print(host_url % img_file_name)
