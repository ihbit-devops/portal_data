import requests
from time import sleep
from datetime import datetime


header = 'asset,amount,createDate'

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiNzZmNTNmZWIxY2EzNGZkY2FhYWE1YTcyZTAxODRiZDQiLCJ0diI6MCwiaWF0IjoxNjY2MDczMzA0LCJleHAiOjE2NjYwODc3MDR9.3eRVG5tLv9K5fuKSmtsF8TNL_d1uH79B4Dn-rhFb1oc',
  'language': 'en'
}

with open('./busd_withdraw_p2p_sep_oct.csv', 'a') as the_file:
    the_file.write('{}\n'.format(header))
    for _ in range(0, 100000, 200):
        url = "https://www.x-meta.com/bc/v1/exchange/spot-withdraw-record?startTime=1662825600000&endTime=1666022400000&status=10&asset=BUSD&offset={}&limit=200".format(_)
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
