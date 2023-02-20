import requests
from time import sleep
from datetime import datetime

import boto3

header = 'uid,email,address'

ssm = boto3.client('ssm')

# header = 'email,id'
token = ssm.get_parameter(Name='/portal/token', WithDecryption=True)['Parameter']['Value']
headers = {
  'Authorization': f'Bearer {token}',
  'language': 'en'
}

with open('./user_email_25.csv', 'a') as the_file:
    # the_file.write('{}\n'.format(header))
    for _ in range(0, 70000, 200):
        url = "https://www.x-meta.com/bc/v1/exchange/customers?offset={}&limit=200".format(_)
        response = requests.request("GET", url, headers=headers)
        
        data = response.json()

        try:
            assert data['code'] == 0
        except:
            sleep(15)
            response = requests.request("GET", url, headers=headers)
        
        if len(data["data"]["userList"]) == 0:
            break

        for user in data['data']['userList']:
            # crtObj = datetime.fromtimestamp(int(user['createTime']) // 1000)
            # createdDate = crtObj.strftime('%Y-%m-%d')
            # iso = crtObj.isoformat()
            row = f"{user['uid']},{user['email']}\n"
            the_file.write(row)
        
        print(f'{_} - {len(data["data"]["userList"])}')


# for _ in range(0, 65000, 300):
#     url = "https://www.x-meta.com/bc/v1/exchange/customers?offset={}&limit=300".format(_)
#     response = requests.request("GET", url, headers=headers)
    
#     data = response.json()
#     try:
#         assert data['code'] == 0
#     except:
#         sleep(15)
#         response = requests.request("GET", url, headers=headers)

#     for user in data['data']['userList']:
#         crtObj = datetime.fromtimestamp(int(user['createTime']) // 1000)
#         createdDate = crtObj.strftime('%Y-%m-%d')

#         row = f"{createdDate}\n"
#         print(row)
    
#     print(f'{_} - {len(data["data"]["userList"])}')
