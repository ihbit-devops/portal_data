import requests
from time import sleep
from datetime import datetime

import boto3


ssm = boto3.client('ssm')

token = ssm.get_parameter(Name='/portal/token', WithDecryption=True)['Parameter']['Value']
headers = {
  'Authorization': f'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiMWJkNDRmZDJmZmY0NDJjMDhiM2M0YmJjZDFiNzQ5ZTUiLCJ0diI6MCwiaWF0IjoxNjc2MDI0NTc1LCJleHAiOjE2NzYwMzg5NzV9.1wNcJV53MnFx0YNnBzc_bN4cY_CG__4l9OT5UV3oHPQ',
  'language': 'en'
}
header = 'asset,amount,createDate'


with open('./deposit_jan.csv', 'a') as the_file:
    # the_file.write('{}\n'.format(header))
    for _ in range(0, 100000, 200):
        url = "https://www.x-meta.com/bc/v1/exchange/spot-deposit-record?startTime=1672502400000&endTime=1675180800000&status=10&offset={}&limit=200".format(_)
        response = requests.request("GET", url, headers=headers)
        data = response.json()
        
        try:
            assert data['code'] == 0
        except:
            sleep(10)
            response = requests.request("GET", url, headers=headers)

        if len(data["data"]["spotDepositRecord"]) == 0:
            break

        for user in data['data']['spotDepositRecord']:
            crtObj = datetime.fromtimestamp(int(user['createTime']) // 1000)
            createdDate = crtObj.strftime('%Y-%m-%d')

            if user['uid'] == "176570" or user['uid'] == "169586" or user['uid'] == "165055":
                continue

            the_file.write('{},{},{}\n'.format(user['asset'], user['amount'], createdDate))
        
        print(f'{_} - {len(data["data"]["spotDepositRecord"])}')
