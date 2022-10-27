import requests
from time import sleep
from datetime import datetime


header = 'amount,asset,createDate,wallet'

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiYzYzYjE5MzA1ZjQ4NDMzZDg4NzEzMTYzMDk2YWIwNGUiLCJ0diI6MCwiaWF0IjoxNjY2MzQ4Nzk1LCJleHAiOjE2NjYzNjMxOTV9.QfBAUCeJc3y8KDIg5ebIz6NK2iYuNhe5GUCKySQcSs0',
  'language': 'en'
}

with open('./deposit_busd_0910-1021.csv', 'a') as the_file:
    the_file.write('{}\n'.format(header))
    for _ in range(0, 100000, 200):
        url = "https://www.x-meta.com/bc/v1/exchange/spot-deposit-record?startTime=1662739200000&endTime=1666281600000&status=10&asset=BUSD&offset={}&limit=200".format(_)
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

            the_file.write('{},{},{}\n'.format(user['amount'], user['asset'], createdDate, day_of_week))
        
        print(f'{_} - {len(data["data"]["spotDepositRecord"])}')


# with open('./withdraw_usdt_0910-1021.csv', 'a') as the_file:
#     the_file.write('{}\n'.format(header))
#     for _ in range(0, 10000, 200):
#         url = "https://www.x-meta.com/bc/v1/exchange/spot-withdraw-record?startTime=1662739200000&endTime=1666281600000&status=10&asset=USDT&offset={}&limit=200".format(_)
#         response = requests.request("GET", url, headers=headers)
#         data = response.json()   

#         try:
#             assert data['code'] == 0
#         except:
#             sleep(10)
#             response = requests.request("GET", url, headers=headers)

#         if len(data["data"]["spotWithdrawRecord"]) == 0:
#             break

#         for user in data['data']['spotWithdrawRecord']:
#             crtObj = datetime.fromtimestamp(int(user['createTime']) // 1000)
#             createdDate = crtObj.strftime('%Y-%m-%d')
#             day_of_week = crtObj.strftime('%A')

#             the_file.write('{},{},{},{}\n'.format(user['amount'], user['asset'], createdDate, user['address']))
        
#         print(f'{_} - {len(data["data"]["spotWithdrawRecord"])}')


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
