import requests
import json
from time import sleep
from datetime import datetime

header = 'tradeId,orderId,symbol,price,qty,quoteQty,commission,commissionAsset,tradeDirection,createTime,updateTime'

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiYzRmMDc3MGY4OGEyNDI5Mzk5YjhiYWIxMGIwZDA2OGEiLCJ0diI6MCwiaWF0IjoxNjY2MjQ0NjQzLCJleHAiOjE2NjYyNTkwNDN9.y7BGvxN2a54zJhVpkEiW-9uoMhOaxxqk_F_0sfrH780',
  'language': 'en'
}


with open('./march.csv', 'a') as the_file:
    the_file.write('{}\n'.format(header))
    
    for _ in range(0, 1000000, 500):
        url = "https://www.x-meta.com/bc/v1/exchange/trade-records?startTime=1646064000000&endTime=1648742399000&offset={}&limit=500".format(_)
        response = requests.request("GET", url, headers=headers)

        data = response.json()

        try:
            assert data['code'] == 0
        except:
            sleep(15)
            response = requests.request("GET", url, headers=headers)
        
        if len(data["data"]["tradeRecords"]) == 0:
            print('finished!.')
            break

        for trade in data['data']['tradeRecords']:
            crtObj = datetime.fromtimestamp(int(trade['createTime']) // 1000)
            createdDate = crtObj.strftime('%Y-%m-%d-%H-%M')

            updateObj = datetime.fromtimestamp(int(trade['updateTime']) // 1000)
            updatedDate = updateObj.strftime('%Y-%m-%d-%H-%M')
            row = f"{trade['tradeId']},{trade['orderId']},{trade['symbol']},{trade['price']},{trade['qty']},{trade['quoteQty']},{trade['commission']},{trade['commissionAsset']},{trade['tradeDirection']},{createdDate},{updatedDate}\n"
            the_file.write(row)

        print(f'{_} - {len(data["data"]["tradeRecords"])}')
