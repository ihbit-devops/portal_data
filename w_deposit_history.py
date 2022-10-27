import requests
from time import sleep
from datetime import datetime


# header = 'uid,asset,amount,createDate,day,txId,depositId'

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiZWJkZjhiYjZlYjdhNDRjYmI3ZGFhMzg3MDIzZDYwM2EiLCJ0diI6MCwiaWF0IjoxNjY2MDkwMTk5LCJleHAiOjE2NjYxMDQ1OTl9.b_8Hij000FPdvEpDh3jl0msDcfq6MElbFiygSVHneZc',
  'language': 'en'
}

with open('./deposit_xmetapool.csv', 'a') as the_file:
    # the_file.write('{}\n'.format(header))
    for _ in range(0, 100000, 200):
        url = "https://www.x-meta.com/bc/v1/exchange/spot-deposit-record?keyword=operation@x-meta.com&startTime=1640966400000&endTime=1666022400000&status=10&offset={}&limit=200".format(_)
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
            day_of_week = crtObj.strftime('%A')

            the_file.write('{},{},{},{},{},{},{}\n'.format(user['uid'], user['asset'], user['amount'], createdDate, day_of_week, user['txId'], user['depositId']))
        
        print(f'{_} - {len(data["data"]["spotDepositRecord"])}')
