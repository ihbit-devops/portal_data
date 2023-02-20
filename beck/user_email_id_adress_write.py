import requests
from time import sleep

import boto3

dynamo = boto3.client('dynamodb')
header = 'uid,email,address'

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiOTUyNGIyYmMzOWJjNDNjODkxYTVjNTIwNDQzY2I3ZmUiLCJ0diI6MCwiaWF0IjoxNjY4NDE2MzgxLCJleHAiOjE2Njg0MzA3ODF9.niPXxnclz9uLemEUurclV6Nrle_urww41Ds6GIj3QeQ',
  'language': 'en'
}

for _ in range(25600, 66000, 200):
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
        response = dynamo.put_item(
            Item={
                "email": {
                    "S": user['email']
                },
                "uid": {
                    "S": user['uid']
                }
            },
            ReturnConsumedCapacity='TOTAL',
            TableName='users_data',
        )
        
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
