from re import L
import requests
import time
import json
from time import sleep
from datetime import datetime

import boto3

ssm = boto3.client('ssm')


header = 'email,id'
token = ssm.get_parameter(Name='/portal/token', WithDecryption=True)['Parameter']['Value']
headers = {
  'Authorization': f'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiMjI3ZDJmM2I5YzMxNDc5MjlmY2M2MmQzNzg2ZDE4ODQiLCJ0diI6MCwiaWF0IjoxNjc2MjcwMTY1LCJleHAiOjE2NzYyODQ1NjV9.OxgzHZwTs0O-tI8FbGmLpfwDzAbyp-BcT9DYjx_KdTo',
  'language': 'en'
}

# User Ids
# with open('./user_emails.csv', 'a') as the_file:
#     # the_file.write('{}\n'.format(header))
#     for _ in range(65533, 68000, 200):
#         url = "https://www.x-meta.com/bc/v1/exchange/customers?offset={}&limit=200".format(_)
#         response = requests.request("GET", url, headers=headers)
#         data = response.json()

#         try:
#             assert data['code'] == 0
#         except:
#             time.sleep(15)
#             response = requests.request("GET", url, headers=headers)
#             data = response.json()
        
#         if len(data["data"]["userList"]) == 0:
#             print('Finished!.')
#             break

#         for user in data['data']['userList']:
#             row = f"{user['uid']},{user['email']}\n"
#             the_file.write(row)
        
#         print(f'{_} - {len(data["data"]["userList"])}')


# IHC BALANCE
# above_5ml_ihc = 0
# above_10ml_ihc = 0
# above_50ml_ihc = 0

with open('./uids_to.csv', 'r') as the_file:
    # the_file.readline()
    lines = the_file.readlines()
    for line in lines:
        line = line.strip()
        
        url = "https://www.x-meta.com/bc/v1/exchange/customer/asset?uid={}".format(line)
        response = requests.request("GET", url, headers=headers)
        data = response.json()
        
        try:
            assert data['code'] == 0
        except:
            sleep(15)
            token = ssm.get_parameter(Name='/portal/token', WithDecryption=True)['Parameter']['Value']
            headers = {
                'Authorization': f'Bearer {token}',
                'language': 'en'
            }

            url = "https://www.x-meta.com/bc/v1/exchange/customer/asset?uid={}".format(line)
            response = requests.request("GET", url, headers=headers)
            data = response.json()

        if data['code'] == 403:
            print(f'Session expired last at {line.strip()}, {data}')
            token = ssm.get_parameter(Name='/portal/token', WithDecryption=True)['Parameter']['Value']
            headers = {
                'Authorization': f'Bearer {token}',
                'language': 'en'
            }

            url = "https://www.x-meta.com/bc/v1/exchange/customer/asset?uid={}".format(line)
            response = requests.request("GET", url, headers=headers)
            data = response.json()
            try:
                assert data['code'] == 0
            except:

                sleep(15)
                response = requests.request("GET", url, headers=headers)

        with open('./ihc_balances.csv', 'a') as the_file:
            for asset in data['data']['assetList']:
                if asset['asset'] == 'IHC':
                    asset_ihc_balance = float(asset['free']) + float(asset['locked'])
                    # text = f'{email},{asset_ihc_balance},{above_5ml_ihc},{above_10ml_ihc},{above_50ml_ihc}'

                    # if asset_ihc_balance >= 50000000:
                    #     above_50ml_ihc += 1
                    #     the_file.write('{}\n'.format(text))

                    # elif asset_ihc_balance >= 10000000:
                    #     above_10ml_ihc += 1
                    #     the_file.write('{}\n'.format(text))
                        
                    # elif asset_ihc_balance >= 5000000:
                    #     above_5ml_ihc += 1
                    #     the_file.write('{}\n'.format(text))

                    text = f'{line},{asset_ihc_balance}'
                    the_file.write('{}\n'.format(text))
                    print(text)


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
