import requests
from time import sleep
from datetime import datetime

header = 'asset,amount,createDate'
headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiYmVkNWJiMDdjNzc5NDM5Y2I2N2UzMDc3OTJmZGNmODUiLCJ0diI6MCwiaWF0IjoxNjY2MTU3NTE4LCJleHAiOjE2NjYxNzE5MTh9.xtG3EpA9JJzk7-Uqa2bL1TLtehpmh8658bu0gWHUYaI',
  'language': 'en'
}

count = 0

with open('./operation_busd_with.csv', 'a') as the_file:
    # the_file.write('{}\n'.format(header))
    for _ in range(0, 1000000, 200):
        url = "https://www.x-meta.com/bc/v1/exchange/spot-withdraw-record?keyword=operation@x-meta.com&startTime=1640966400000&endTime=1666108800000&status=10&asset=BUSD&offset={}&limit=200".format(_)
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

            if user['address'] == "0x5f276b8a5085c49b6a2fb99be2a72870c14f58c6":
                count+=1
                print(f'------------{count}----------------')
                continue
            the_file.write('{},{},{}\n'.format(user['asset'], user['amount'], createdDate))
        
        print(f'{_} - {len(data["data"]["spotWithdrawRecord"])}')

