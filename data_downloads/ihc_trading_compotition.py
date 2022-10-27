import requests
from time import sleep
from datetime import datetime

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiOWYwYjI4N2EzM2ZkNGZlYjkzOWUzY2IwY2MwNTYwZTQiLCJ0diI6MCwiaWF0IjoxNjU4MjgxOTM4LCJleHAiOjE2NTgyOTYzMzh9.tNRKefOOcs9kAxx8PmTiyXi8IHPw0yD5JdIfXOyveD4',
  'language': 'en'
}

total_reward = 0
total_partipicants = 0

with open('./results.csv', 'r') as the_file:
    the_file.readline()
    for _ in the_file.readlines():
        sleep(1)
        email = _.split(',')[0].replace('"', '', 2)

        total_partipicants += 1
        total_trade_volume = 0

        url = f"https://www.x-meta.com/bc/v1/exchange/trade-records?keyword={email}&asset=IHC&startTime=1657728000000&endTime=1658160000000&offset=0&limit=500"
        response = requests.request("GET", url, headers=headers)
        try:
            data = response.json()
        except:
            print(f'{email},0,0,0')

        try:
            assert data['code'] == 0
        except:
            sleep(15)
            response = requests.request("GET", url, headers=headers)
        
        buy_sum = 0
        sell_sum = 0
        uid = None
        asset_ihc_balance = 0

        for trade in data['data']['tradeRecords']:
            uid = trade['uid']
            total_trade_volume += float(trade['qty'])
            if trade['tradeDirection'].lower() == 'sell':
                sell_sum += float(trade['qty'])
            else:
                buy_sum += float(trade['qty'])
        
        trading_balance_ihc = buy_sum - sell_sum

        if len(data['data']['tradeRecords']) == 0:
            print(f'{email},0,0,0')

        reward_ihc_qty = 0
        reward_ihc_qty = (trading_balance_ihc * 1.01) / 100

        # Balance part
        if uid is not None:
            url = "https://www.x-meta.com/bc/v1/exchange/customer/asset?uid={}".format(uid)
            response = requests.request("GET", url, headers=headers)
            data = response.json()

            try:
                assert data['code'] == 0
            except:

                sleep(15)
                response = requests.request("GET", url, headers=headers)

            for asset in data['data']['assetList']:
                if asset['asset'] == 'IHC':
                    asset_ihc_balance = float(asset['free'])
            
            
            if (asset_ihc_balance - trading_balance_ihc) > 0:
                print(f'UID:{uid}, TradeBalance:{trading_balance_ihc},AssetBalance:{asset_ihc_balance},Reward:{reward_ihc_qty},Total Trade Volume: {total_trade_volume},Confirmed')

        else:
            print(f'NO UID: check Balance -> {email}, trade balance: {trading_balance_ihc}, reward: {reward_ihc_qty}, Total Trade Volume: {total_trade_volume}')
        
        total_reward += reward_ihc_qty
    
    print(f'FINISHED: {total_reward} - {total_partipicants}')
