import requests
from time import sleep
from datetime import datetime


header = 'txId,amount,asset,createDate'

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiNzQxNzc2YWExZDVjNDhhYzlhNTVmNTg5NjA4MzJhMDUiLCJ0diI6MCwiaWF0IjoxNjc0MTE5MDA5LCJleHAiOjE2NzQxMzM0MDl9.C_1a_vtMraxZrEpH8IcH8KFPyC_dYx0lNBUKvKzvzn4',
  'language': 'en'
}

# with open('./deposit_operation_22.csv', 'a') as the_file:
#     # the_file.write('{}\n'.format(header))
#     for _ in range(0, 100000, 200):
#         url = "https://www.x-meta.com/bc/v1/exchange/spot-deposit-record?keyword=xmetapool@x-meta.com&startTime=1640966400000&endTime=1672502400000&offset={}&limit=200".format(_)
#         response = requests.request("GET", url, headers=headers)
#         data = response.json()

#         try:
#             assert data['code'] == 0
#         except:
#             sleep(10)
#             response = requests.request("GET", url, headers=headers)

#         if len(data["data"]["spotDepositRecord"]) == 0:
#             break

#         for user in data['data']['spotDepositRecord']:
#             crtObj = datetime.fromtimestamp(int(user['createTime']) // 1000)
#             createdDate = crtObj.strftime('%Y-%m-%d')

#             the_file.write('{},{},{}\n'.format(user['amount'], user['asset'], createdDate))
        
#         print(f'{_} - {len(data["data"]["spotDepositRecord"])}')


with open('./withdraw_operation_22_txid.csv', 'a') as the_file:
    # the_file.write('{}\n'.format(header))
    for _ in range(0, 100000, 200):
        url = "https://www.x-meta.com/bc/v1/exchange/spot-withdraw-record?keyword=xmetapool@x-meta.com&startTime=1640966400000&endTime=1672502400000&status=10&offset={}&limit=200".format(_)
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
            
            the_file.write('{},{},{},{}\n'.format(user['txId'], user['amount'], user['asset'], createdDate))
        
        print(f'{_} - {len(data["data"]["spotWithdrawRecord"])}')


# with open('./deposit_3-4_usdt.csv', 'a') as the_file:
#     the_file.write('{}\n'.format(header))
#     for _ in range(0, 30000, 200):
#         url = f"https://www.x-meta.com/bc/v1/exchange/spot-deposit-record?startTime=1646064000000&endTime=1651334399000&asset=USDT&offset={_}&limit=200".format(_)
#         response = requests.request("GET", url, headers=headers)
#         data = response.json()   

#         try:
#             assert data['code'] == 0
#         except:
#             sleep(10)
#             response = requests.request("GET", url, headers=headers)

#         for user in data['data']['spotDepositRecord']:
#             crtObj = datetime.fromtimestamp(int(user['createTime']) // 1000)
#             createdDate = crtObj.strftime('%Y-%m-%d')

#             the_file.write('{},{},{}\n'.format(user['amount'], user['asset'], createdDate))
        
#         print(f'{_} - {len(data["data"]["spotDepositRecord"])}')


# with open('./deposit_5-6_usdt.csv', 'a') as the_file:
#     the_file.write('{}\n'.format(header))
#     for _ in range(0, 30000, 200):
#         url = f"https://www.x-meta.com/bc/v1/exchange/spot-deposit-record?startTime=1651334400000&endTime=1653580799000&asset=USDT&offset={_}&limit=200".format(_)
#         response = requests.request("GET", url, headers=headers)
#         data = response.json()   

#         try:
#             assert data['code'] == 0
#         except:
#             sleep(10)
#             response = requests.request("GET", url, headers=headers)

#         for user in data['data']['spotDepositRecord']:
#             crtObj = datetime.fromtimestamp(int(user['createTime']) // 1000)
#             createdDate = crtObj.strftime('%Y-%m-%d')

#             the_file.write('{},{},{}\n'.format(user['amount'], user['asset'], createdDate))
        
#         print(f'{_} - {len(data["data"]["spotDepositRecord"])}')
