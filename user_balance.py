

from itertools import tee
import requests
import time
import json
from time import sleep
from datetime import datetime
import sys

header = 'email,id'

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiNWI2MmQ5MmExMzNmNGE2YzllYTI3YTU1N2ZiZjVjYjUiLCJ0diI6MCwiaWF0IjoxNjY0MzM3MTM2LCJleHAiOjE2NjQzNTE1MzZ9.MaYILjSJxSHrXA_ObJ-sO47SXIs4zOCLCRBeQEv8WnE',
  'language': 'en'
}

# User Ids
with open('./user_emails.csv', 'a') as the_file:
    the_file.write('{}\n'.format(header))
    for _ in range(0, 66000, 100):
        url = "https://www.x-meta.com/bc/v1/exchange/customers?offset={}&limit=100".format(_)
        response = requests.request("GET", url, headers=headers)
        data = response.json()

        try:
            assert data['code'] == 0
        except:
            time.sleep(15)
            response = requests.request("GET", url, headers=headers)
            data = response.json()
        
        if len(data["data"]["userList"]) == 0:
            print('Finished!.')
            break

        for user in data['data']['userList']:
            row = f"{user['uid']},{user['email']}\n"
            the_file.write(row)
        
        print(f'{_} - {len(data["data"]["userList"])}')


# IHC BALANCE
# above_5ml_ihc = 3056

# with open('./user_ids.csv', 'r') as the_file:
#     lines = the_file.readlines()
#     for line in lines:
#         url = "https://www.x-meta.com/bc/v1/exchange/customer/asset?uid={}".format(line.strip())
#         response = requests.request("GET", url, headers=headers)
#         data = response.json()

#         try:
#             assert data['code'] == 0
#         except:

#             sleep(15)
#             response = requests.request("GET", url, headers=headers)

#         if data['code'] == 403:
#             print(f'Session expired last at {line.strip()}, {data}')

#         with open('./ihc_balance.csv', 'a') as the_file:
#             for asset in data['data']['assetList']:
#                 if asset['asset'] == 'IHC':
#                     asset_ihc_balance = float(asset['free'])
#                     text = f'{line.strip()},{asset_ihc_balance},{above_5ml_ihc}'
#                     print(text)
#                     the_file.write('{}\n'.format(text))

#                     if asset_ihc_balance > 5000000:
#                         above_5ml_ihc += 1
#     print(f'Number: {above_5ml_ihc}')



# ALL TOKEN BALANCE
# with open('./lastIndex.csv', 'r') as the_file:
#     line = the_file.readline()
#     last_line = int(line.strip())
#     print(f'READ LAST ROW INDEX: {last_line}')

# with open('./user_ids.csv', 'r') as the_file:
#     lines = the_file.readlines()
#     for line in lines[last_line:]:
#         try:
#             try:
#                 url = "https://www.x-meta.com/bc/v1/exchange/customer/asset?uid={}".format(line.strip())
#                 response = requests.request("GET", url, headers=headers)
#                 data = response.json()
#                 assert data['code'] == 0
#                 last_line += 1
#             except:
#                 sleep(15)
#                 response = requests.request("GET", url, headers=headers)

#             if data['code'] != 0:
#                 print(f'ERROR: {line.strip()}, {data}')
#                 with open('./lastIndex.csv', 'w') as the_file:
#                     text = f'Last Row: {last_line}'
#                     print(text)
#                     the_file.write(f'{last_line}')
#                     break

#             with open('./user_balance.csv', 'a') as the_file:
#                 for asset in data['data']['assetList']:
#                     text = f'{line.strip()},{asset["asset"]},{float(asset["free"])},{float(asset["locked"])}'
#                     print(text)
#                     the_file.write('{}\n'.format(text))
#         except:
#             with open('./lastIndex.csv', 'w') as the_file:
#                 text = f'Last Row: {last_line}'
#                 print(text)
#                 the_file.write(f'{last_line}')
