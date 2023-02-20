import requests
import time
import json
from time import sleep
from datetime import datetime

header = 'uid,phone'

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiMDY1NzBhOGVhZWZhNGFjNmI3ZGMyMTkwN2Q4NGU1NzYiLCJ0diI6MCwiaWF0IjoxNjc2MzY3NjQyLCJleHAiOjE2NzYzODIwNDJ9.5FCO_tPpD2lr0Gqk5tnEhPqgYWkBxmJT2NrgxUbTFXA',
  'language': 'en'
}

with open('./user_kyc_info.csv', 'a') as the_file:
    the_file.write('{}\n'.format(header))
    for _ in range(0, 65000, 200):
        url = "https://www.x-meta.com/bc/v1/exchange/common-kyc/user-list?status=10&offset={}&limit=200".format(_)
        response = requests.request("GET", url, headers=headers)
        data = response.json()
        
        try:
            assert data['code'] == 0
        except:
            time.sleep(15)
            response = requests.request("GET", url, headers=headers)
            data = response.json()
        
        if len(data["data"]["userKycInfos"]) == 0:
            break

        for user in data['data']['userKycInfos']:

            # updatedObj = datetime.fromtimestamp(int(user['updateTime']) // 1000)
            # updatedDate = updatedObj.strftime('%Y-%m-%d')
            # iso = updatedObj.isoformat()
            
            row = f"{user['uid']},{user['phone']}\n"
            the_file.write(row)
        print(f'{_} - {len(data["data"]["userKycInfos"])}')
