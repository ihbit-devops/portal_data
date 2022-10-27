import requests
from time import sleep
from datetime import datetime
import math

header = 'uid,asset,price,mnt_price,amount,mnt_amount,network,address,createDate,finishDate'
busd_rate = 3378.10
given_date = '24'
prices = {
    'BUSD': 1,
    'USDT': 1
}

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjMwLCJzaWduIjoiYWI3NzA1YmY3MGYzNDBmNGI2NDliYjcyMzEwMjEyNjMiLCJ0diI6MCwiaWF0IjoxNjY2NzY1ODA1LCJleHAiOjE2NjY3ODAyMDV9.ry-wkllp5j0MgGd-kHDTnWST-tZAZoAmoKZZASZ2cFY',
  'language': 'en'
}

with open('./deposit_{}.csv'.format(given_date), 'a') as the_file:
    the_file.write('{}\n'.format(header))
    for _ in range(0, 100000, 200):
        url = "https://www.x-meta.com/bc/v1/exchange/spot-deposit-record?startTime=1666540800000&endTime=1666713600000&status=10&offset={}&limit=200".format(_)
        response = requests.request("GET", url, headers=headers)
        data = response.json()
        
        try:
            assert data['code'] == 0
        except:
            sleep(10)
            response = requests.request("GET", url, headers=headers)

        if len(data["data"]["spotDepositRecord"]) == 0:
            break

        for deposit in data['data']['spotDepositRecord']:
            crt_obj = datetime.fromtimestamp(int(deposit['createTime']) // 1000)
            created_date = crt_obj.strftime('%Y.%m.%d')

            fns_obj = datetime.fromtimestamp(int(deposit['finishTime']) // 1000)
            finish_date = fns_obj.strftime('%Y.%m.%d')


            if deposit['asset'] not in prices:
                url = "https://www.x-meta.com/open/v1/market/depth?symbol={}_BUSD&limit=10".format(deposit['asset'])
                response = requests.request("GET", url, headers=headers)
                price_data = response.json()
                
                if price_data['code'] != 0:
                    prices[deposit['asset']] = 0
                else:
                    asset_current_price_busd = price_data['data']['asks'][0][0]
                    prices[deposit['asset']] = float(asset_current_price_busd)
            
            mnt_price = math.ceil((prices[deposit['asset']] * busd_rate) * 100) / 100
            mnt_value = math.ceil(float(deposit['amount']) * mnt_price)

            if mnt_value >= 20000000:
                the_file.write('{},{},{},{},{},{},{},{},{},{}\n'.format(deposit['uid'], deposit['asset'], prices[deposit['asset']], 
                    mnt_price, deposit['amount'], mnt_value, deposit['network'], deposit['address'], created_date, finish_date))
        
        print(f'{_} - {len(data["data"]["spotDepositRecord"])}')


with open('./withdraw_{}.csv'.format(given_date), 'a') as the_file:
    the_file.write('{}\n'.format(header))
    for _ in range(0, 100000, 200):
        url = "https://www.x-meta.com/bc/v1/exchange/spot-withdraw-record?startTime=1666540800000&endTime=1666627200000&status=10&offset={}&limit=200".format(_)
        response = requests.request("GET", url, headers=headers)
        data = response.json()
        
        try:
            assert data['code'] == 0
        except:
            sleep(10)
            response = requests.request("GET", url, headers=headers)

        if len(data["data"]["spotWithdrawRecord"]) == 0:
            break

        for withdraw in data['data']['spotWithdrawRecord']:
            crt_obj = datetime.fromtimestamp(int(withdraw['createTime']) // 1000)
            created_date = crt_obj.strftime('%Y.%m.%d')

            fns_obj = datetime.fromtimestamp(int(withdraw['finishTime']) // 1000)
            finish_date = fns_obj.strftime('%Y.%m.%d')

            if withdraw['uid'] == "176570" or withdraw['uid'] == "169586":
                print('SKIPPED!.')
                continue

            if withdraw['asset'] not in prices:
                url = "https://www.x-meta.com/open/v1/market/depth?symbol={}_BUSD&limit=10".format(withdraw['asset'])
                response = requests.request("GET", url, headers=headers)
                price_data = response.json()
                
                if price_data['code'] != 0:
                    prices[withdraw['asset']] = 0
                else:
                    asset_current_price_busd = price_data['data']['asks'][0][0]
                    prices[withdraw['asset']] = float(asset_current_price_busd)
            
            mnt_price = math.ceil((prices[withdraw['asset']] * busd_rate) * 100) / 100
            mnt_value = math.ceil(float(withdraw['amount']) * mnt_price)

            if mnt_value >= 20000000:
                the_file.write('{},{},{},{},{},{},{},{},{},{}\n'.format(withdraw['uid'], withdraw['asset'], prices[withdraw['asset']], 
                    mnt_price, withdraw['amount'], mnt_value, withdraw['network'], withdraw['address'], created_date, finish_date))
        
        print(f'{_} - {len(data["data"]["spotWithdrawRecord"])}')
