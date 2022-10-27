import requests
from time import sleep
from datetime import datetime

header = 'symbol,price,qty,quoteQty,commission,commissionAsset,tradeDirection,createTime,updateTime'

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiMjA5ODk0M2VhNjYzNDQ5Nzk4Y2Q0OWFlOTNhMmZjM2UiLCJ0diI6MCwiaWF0IjoxNjY0ODUwMTk5LCJleHAiOjE2NjQ4NjQ1OTl9.puVkN4KahbuoPh2xbzDJXhCHPh0rTnf0ZAnPm4K-pN0',
  'language': 'en'
}


with open('./trade_19-23.csv', 'a') as the_file:
    # the_file.write('{}\n'.format(header))
    
    for _ in range(0, 1000000, 500):
        url = "https://www.x-meta.com/bc/v1/exchange/trade-records?startTime=1663516800000&endTime=1663948799000&settleStatus=10&offset={}&limit=500".format(_)
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
            # if trade['tradeDirection'].lower() == 'sell':
            crtObj = datetime.fromtimestamp(int(trade['createTime']) // 1000)
            createdDate = crtObj.strftime('%Y-%m-%d-%H-%M')

            updateObj = datetime.fromtimestamp(int(trade['updateTime']) // 1000)
            updatedDate = updateObj.strftime('%Y-%m-%d-%H-%M')
            row = f"{trade['symbol']},{trade['price']},{trade['qty']},{trade['quoteQty']},{trade['commission']},{trade['commissionAsset']},{trade['tradeDirection']},{createdDate},{updatedDate}\n"
            the_file.write(row)
        
        print(f'{_} - {len(data["data"]["tradeRecords"])}')
