import json
import requests


headers = {
    'Content-Type': 'application/json; charset=UTF-8',
    'CSRFToken': 'arbitrary_token',
    'Cookie': 'CSRFToken=arbitrary_token; ASP.NET_SessionId=0tkrkvxiqmfpl0cl143x4f5s',
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

response = requests.post(
    'https://ezpost.post.gov.tw/WCFService.svc/InsertNewMailInfoNolLogin',
    headers=headers,
    data=json.dumps(payload)
)

resp_json = response.json()
try:
    mail_no = json.loads(resp_json['d'])['Message']
except:
    print('Cannot fetch the MailNo. Stopped.')
    exit(1)


headers = {
    'Content-Type': 'application/json; charset=UTF-8',
    'CSRFToken': 'arbitrary_token',
    'Cookie': 'CSRFToken=arbitrary_token; ASP.NET_SessionId=0tkrkvxiqmfpl0cl143x4f5s',
}

payload = {
    'MailNo': mail_no,
}

response = requests.post(
    'https://ezpost.post.gov.tw/PrintPdf.aspx',
    data=json.dumps(payload),
    headers=headers,
    allow_redirects=True
)
output_pdf_file = '%s.pdf' % payload['MailNo']
with open(output_pdf_file, 'wb') as f:
    f.write(response.content)


print('The %s file is saved!' % output_pdf_file)
