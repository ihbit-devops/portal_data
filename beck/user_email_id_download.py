import requests
from time import sleep
from datetime import datetime

header = 'uid,email,address'

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiODM2MjIxNjFiYjY4NDRiNWJkMmNhMTVlYmU0NjJjMWMiLCJ0diI6MCwiaWF0IjoxNjYyNDMxODk0LCJleHAiOjE2NjI0NDYyOTR9.VV5NcxIvndUjhjQTfUiwdZkdaOODEveEQTnUrybHs9o',
  'language': 'en'
}

with open('./email_and_uid_address.csv', 'a') as the_file:
    the_file.write('{}\n'.format(header))
    for _ in range(0, 65000, 200):
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
            row = f"{user['uid']},{user['email']},{user['address']}\n"
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
