import requests
import time
import json
from time import sleep
import datetime

header = 'symbol,listDate,fullname'

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjIsInNpZ24iOiJjNWYwZWM5NDhlNDY0ZTNhYWRiNmU4ZTM1NDMwNWY3NiIsInR2IjowLCJpYXQiOjE2NzM5NDA3NTUsImV4cCI6MTY3Mzk1NTE1NX0.3aO_eXzlrpsVznlN5SMFkuTa1ZYOQtEEPKmDTgb4qoE',
  'language': 'en'
}

currencies = {}

with open('./tokens.csv', 'r') as the_file:
    print(the_file.readline())
    
    for line in the_file.readlines():
        lines = line.split(',')

        if 'n' in lines[3].strip().lower():
            continue
        print(line)

        if ':' not in lines[1].strip():
            # datetime_iso = datetime.datetime.strptime(lines[1].strip(), "%Y-%m-%d %H:%M:%S")
            lines[1] += ' 20:02:22'
        
        if lines[5].replace('"', '').replace('"', '').strip() == '' or lines[3].strip() == '':
            continue

        currencies[lines[0]] = {
            'symbol': lines[0],
            'listDate': lines[1],
            'name': lines[2].strip(),
            'listMNT': float(lines[5].replace('"', '').replace('"', '').strip()),
            'listUSD': float(lines[3].strip()),
        }
    print(currencies)
    
    # with open('./new_list.csv', 'r') as the_file:
    #     print(the_file.readline())
    #     with open('./new_new_list.csv', 'a') as s_file:
    #         for line in the_file.readlines():
    #             lines = line.split(',')
    #             symbol = lines[0].strip()

    #             if symbol not in currencies:
    #                 s_file.write(f'{line}')



    # the_file.write('{}\n'.format(header))
    # for _ in range(0, 65000, 100):
    #     url = "https://www.x-meta.com/bc/v1/exchange/assets?status=1&offset={}&limit=100".format(_)
    #     response = requests.request("GET", url, headers=headers)
    #     data = response.json()
        
    #     try:
    #         assert data['code'] == 0
    #     except:
    #         time.sleep(15)
    #         response = requests.request("GET", url, headers=headers)
    #         data = response.json()
        
    #     if len(data['data']['assetList']) == 0:
    #         print('FINSHIED!.')
    #         break
        
    #     for asset in data['data']['assetList']:
    #         if asset['statusName'].lower() == 'enabled':
    #             row = f'{asset["assetCode"]},{asset["createTime"]},{""}\n'
    #             the_file.write(row)
        