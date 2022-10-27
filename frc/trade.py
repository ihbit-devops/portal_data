import sys
import requests
import math
from time import sleep
from datetime import datetime, date


header = 'uid,symbol,price,mnt_price,busd_amount,mnt_amount,token_amount,type,createTime,wallet'

busd_rate = 3382.39
given_date = '25'

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjMwLCJzaWduIjoiMjdkZTYwNTYxNTM3NDA0NTg2MjBjMjkxMGE1YjM3MzkiLCJ0diI6MCwiaWF0IjoxNjY2NzUxNDA1LCJleHAiOjE2NjY3NjU4MDV9.5H9hDLKd02l-RHarwEH1r-S7fLg_o1fIRlhIN_XSlPs',
  'language': 'en'
}

with open('./trade_{}.csv'.format(given_date), 'a') as the_file:
    the_file.write('{}\n'.format(header))
    
    for _ in range(0, 1000000, 500):
        url = "https://www.x-meta.com/bc/v1/exchange/trade-records?startTime=1666627200000&endTime=1666713600000&settleStatus=10&offset={}&limit=500".format(_)
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

            price = float(trade['price'])
            amount_busd = float(trade['quoteQty'])
            token_amount = float(trade['qty'])

            mnt_price = math.ceil((price * busd_rate) * 100) / 100
            mnt_amount = math.ceil((amount_busd * busd_rate) * 100) / 100
            wallet = 'n/a'
            
            if mnt_amount >= 20000000:
                url = "https://www.x-meta.com/bc/v1/exchange/customer/asset?uid={}".format(trade['uid'])
                response = requests.request("GET", url, headers=headers)
                wallet_data = response.json()
                if wallet_data['code'] == 0:
                    for wal_addr in wallet_data['data']['depositList']:
                        if wal_addr['asset'] == 'BUSD':
                            wallet = wal_addr['address']

                row = f"{trade['uid']},{trade['symbol']},{price},{mnt_price},{amount_busd},{mnt_amount},{token_amount},{trade['tradeDirection']},{createdDate},{wallet}\n"
                the_file.write(row)
        print(f'{_} - {len(data["data"]["tradeRecords"])}')
