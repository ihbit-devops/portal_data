import requests
from time import sleep
from datetime import datetime


header = 'UID,date'

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjEwLCJzaWduIjoiOTIzNmE5ZGIxZjNjNDExZGFmZjRmMzA4YTQ1Yjk0YTgiLCJ0diI6MCwiaWF0IjoxNjU0MjE2NTI4LCJleHAiOjE2NTQyMzA5Mjh9.7KTaPenboOZmkphfoVVfshIUz9WpVfq6V6-7WUlG5xY'
}

with open('./registered_users.csv', 'a') as the_file:
    the_file.write('{}\n'.format(header))
    for _ in range(0, 62000, 100):
        url = "https://www.x-meta.com/bc/v1/exchange/customers?offset={}&limit=100".format(_)
        response = requests.request("GET", url, headers=headers)
        data = response.json()        

        try:
            assert data['code'] == 0
        except:
            sleep(10)
            response = requests.request("GET", url, headers=headers)

        for user in data['data']['userList']:
            crtObj = datetime.fromtimestamp(int(user['createTime']) // 1000)
            createdDate = crtObj.strftime('%Y-%m-%d')

            the_file.write('{},{}\n'.format(user['uid'], createdDate))
        
        print(f'{_} - {len(data["data"]["userList"])}')


# dynamo = boto3.client('dynamodb')

# def write_to_db(uid, email):
#   url = "https://www.x-meta.com/bc/v1/exchange/customer/asset?uid={}".format(uid)
#   response = requests.request("GET", url, headers=headers)

#   if response.status_code != 200:
#     print(response.status_code)
#     print(response)
#     return
  
#   ihcFree = None
#   ihcLocked = None

#   if response.json()['code'] != 0:
#     print(response.status)
#     return

#   data = response.json()['data']

#   if data['assetList'] == []:
#     print('empty!.')
#     return

#   for asset in response.json()['data']['assetList']:
#     if asset['asset'] == 'IHC':
#       ihcFree = asset['free']
#       ihcLocked = asset['locked']

#   if ihcFree == None or ihcFree == None:
#     print('empty ihc!.')
#     return

#   response = dynamo.put_item(
#               Item={
#                 "uid": {
#                 "S": uid
#                 },
#                 "email": {
#                 "S": email
#                 },
#                 "ihcFree": {
#                 "S": str(ihcFree)
#                 },
#                 "ihcLocked": {
#                 "S": str(ihcLocked)
#                 },
#               },
#               ReturnConsumedCapacity='TOTAL',
#               TableName='xmeta-users1',
#           )
#   print(response)


# with open('./user_info_1.csv', 'r') as the_file:
#   lines = the_file.readlines()

#   for _ in range(0, 53000, 100):
#     thous = lines[_:_ + 100]
#     threads = []

#     for _ in range(100):
#       uid = thous[_].split(',')[1]
#       email = thous[_].split(',')[2]
#       t = threading.Thread(target=write_to_db, args=[uid, email])  # args to do something func
#       t.start()
#       threads.append(t)

#     for thread in threads:
#         thread.join()
    
#     print('DONE!')
#     sleep(1)



