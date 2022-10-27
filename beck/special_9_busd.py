import requests
from time import sleep
from datetime import datetime


header = 'uid,amount,createDate,asset'

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjIyLCJzaWduIjoiZTg4ZWRjNjQxN2E4NDBjNGIwZmJjODUxY2FlNTBiNWIiLCJ0diI6MCwiaWF0IjoxNjY2MDgzOTkxLCJleHAiOjE2NjYwOTgzOTF9.PVL7h4t92oB6LKQryqQGkHDHgg4ap77N-eNgWghmtSw',
  'language': 'en'
}

with open('./9_busd.csv', 'a') as the_file:
    the_file.write('{}\n'.format(header))
    for _ in range(0, 100000, 200):
        url = "https://www.x-meta.com/bc/v1/exchange/operation/account-details?uid=9&startTime=1640966400000&endTime=1666022400000&offset={}&limit=200".format(_)
        response = requests.request("GET", url, headers=headers)
        data = response.json()
       
        try:
            assert data['code'] == 0
        except:
            sleep(10)
            response = requests.request("GET", url, headers=headers)

        if len(data["data"]["detailList"]) == 0:
            break

        for user in data['data']['detailList']:
            crtObj = datetime.fromtimestamp(int(user['createTime']) // 1000)
            createdDate = crtObj.strftime('%Y-%m-%d')
          
            the_file.write('{},{},{},{}\n'.format(user['uid'], user['amount'], createdDate, user['asset']))
        
        print(f'{_} - {len(data["data"]["detailList"])}')
