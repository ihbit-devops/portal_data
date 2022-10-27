import requests
from time import sleep
from datetime import datetime


header = 'asset,amount,createDate'

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiZDUwZjFjMTlhNThjNDEwMzlmMTI5YTUxYTkyYjRjYmIiLCJ0diI6MCwiaWF0IjoxNjYzODEzMjM3LCJleHAiOjE2NjM4Mjc2Mzd9.m-XbR_FDBkOfujTmTER7g5lNDMOE7AP_ZJRsc3jhkMU',
  'language': 'en'
}

with open('./busd-withdraw-busd.csv', 'a') as the_file:
    the_file.write('{}\n'.format(header))
    for _ in range(0, 100000, 200):
        url = "https://www.x-meta.com/bc/v1/exchange/spot-withdraw-record?keyword=operation@x-meta.com&startTime=1662739200000&endTime=1666281600000&status=10&asset=BUSD&offset={}&limit=200".format(_)
        response = requests.request("GET", url, headers=headers)
        data = response.json()
        
        try:
            assert data['code'] == 0
        except:
            sleep(10)
            response = requests.request("GET", url, headers=headers)

        if len(data["data"]["spotWithdrawRecord"]) == 0:
            break

        for user in data['data']['spotWithdrawRecord']:
            crtObj = datetime.fromtimestamp(int(user['createTime']) // 1000)
            createdDate = crtObj.strftime('%Y-%m-%d')
            day_of_week = crtObj.strftime('%A')

            if user['uid'] == "176570" or user['uid'] == "169586":
                continue
            the_file.write('{},{},{}\n'.format(user['asset'], user['amount'], createdDate))
        
        print(f'{_} - {len(data["data"]["spotWithdrawRecord"])}')
