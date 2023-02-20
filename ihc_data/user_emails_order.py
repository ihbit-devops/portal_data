import requests
from time import sleep

import boto3

ssm = boto3.client('ssm')

token = ssm.get_parameter(Name='/portal/token', WithDecryption=True)['Parameter']['Value']
headers = {
  'Authorization': f'Bearer {token}',
  'language': 'en'
}

check_list = []

with open('./order_user_id.csv', 'a') as the_file:
    for _ in range(0, 68000, 200):
        url = "https://www.x-meta.com/bc/v1/exchange/order-records?symbol=IHC_BUSD&side=1&startTime=1667232000000&endTime=1669823999000&startAmount=5000000&endAmount=5000000000&offset={}&limit=200".format(_)
        response = requests.request("GET", url, headers=headers)
        
        data = response.json()

        try:
            assert data['code'] == 0
        except:
            print(data)
            sleep(15)
            response = requests.request("GET", url, headers=headers)
        
        if len(data["data"]["orderRecords"]) == 0:
            break

        for user in data['data']['orderRecords']:
            if user['uid'] not in check_list:
                row = f"{user['uid']},{user['email']}\n"
                the_file.write(row)
                check_list.append(user['uid'])

            
        print(f'{_} - {len(data["data"]["orderRecords"])}')
