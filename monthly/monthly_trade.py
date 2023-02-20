import requests
from time import sleep
from datetime import datetime

import boto3

ssm = boto3.client('ssm')

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiY2VkOGQyOGY3OGNkNDE4YmE3MGJlNDVhZjQ0NDZjZTIiLCJ0diI6MCwiaWF0IjoxNjc2MzU5OTQ1LCJleHAiOjE2NzYzNzQzNDV9.MSjossoL9dB3-HWvskfItFBsKkLmsmuhdbc7JeTSzNY'
headers = {
  'Authorization': f'Bearer {token}',
  'language': 'en'
}

header = 'uid,symbol,price,qty,quoteQty,commission,commissionAsset,tradeDirection,createTime,updateTime'

with open('./ihc_trade_2023_jan-feb.csv', 'a') as the_file:
    the_file.write('{}\n'.format(header))
    
    for _ in range(0, 1000000, 500):
        url = "https://www.x-meta.com/bc/v1/exchange/trade-records?asset=IHC&startTime=1672502400000&endTime=1676390399000&offset={}&limit=500".format(_)
        response = requests.request("GET", url, headers=headers)
        
        data = response.json()

        try:
            assert data['code'] == 0
        except:
            sleep(15)
            response = requests.request("GET", url, headers=headers)
        
        if len(data["data"]["tradeRecords"]) == 0:
            break
            
        for trade in data['data']['tradeRecords']:
            crtObj = datetime.fromtimestamp(int(trade['createTime']) // 1000)
            createdDate = crtObj.strftime('%Y-%m-%d-%H-%M')

            if trade['uid'] == "176570" or trade['uid'] == "169586" or trade['uid'] == "187975":
                print(trade['quoteQty'])
                continue
            
            updateObj = datetime.fromtimestamp(int(trade['updateTime']) // 1000)
            updatedDate = updateObj.strftime('%Y-%m-%d-%H-%M')
            row = f"{trade['uid']},{trade['symbol']},{trade['price']},{trade['qty']},{trade['quoteQty']},{trade['commission']},{trade['commissionAsset']},{trade['tradeDirection']},{createdDate},{updatedDate}\n"
            the_file.write(row)

        print(f'{_} - {len(data["data"]["tradeRecords"])}')
