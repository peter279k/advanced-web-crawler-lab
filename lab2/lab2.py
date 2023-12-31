import json
import requests


requests_session = requests.Session()
requests_session.get('https://ezpost.post.gov.tw/Index.html?r=540335')


headers = {
    'Content-Type': 'application/json; charset=UTF-8',
}

payload = {
    'SName': '李昀陞',
    'SPHONE': '0905285349',
    'SADDCity': '臺北市',
    'SADDArea': '松山區',
    'SADDRoad': '民生東路四段',
    'SADDOther': '台北市松山區民生東路四段133號',
    'SADDZIP': '105',
    'SEMAIL': 'peter279k@gmail.com',

    'RName': '李昀陞',
    'RPHONE': '0905285349',
    'RADDCity': '臺北市',
    'RADDArea': '松山區',
    'RADDRoad': '民生東路四段',
    'RADDOther': '台北市松山區民生東路四段133號',
    'RADDZIP': '105',
    'RADDType': '001',
    'RADD_iBox_ADMId': '',
    'MAIL_DEPTH': '1',
    'MAIL_WIDTH': '1',
    'MAIL_HEIGHT': '1',
    'CONTENTS_NO': '6',
    'CONTENTS': '',
    'COMMENT': '',
    'UnDeliverOptNo': 2,
}

response = requests_session.post(
    'https://ezpost.post.gov.tw/WCFService.svc/InsertNewMailInfoNolLogin',
    headers=headers,
    data=json.dumps(payload)
)

print(response.text)
