import requests
from time import sleep
from datetime import datetime
import json


# data_best = {}
# with open('./withdraw_to_binance_best.json', 'r') as the_file:
#     data_best = the_file.readline()
#     data_best = json.loads(data_best)
#     print(data_best)

#     with open('./withdraws_with_amount.csv', 'a') as f_csv:
#         for k, v in data_best.items():
#             f_csv.write(f'{k},{v}\n')


headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiOGRkMjExYWI5ODU2NDZlZGJiNmFlYTNhYzEyZTA5YTUiLCJ0diI6MCwiaWF0IjoxNjYxOTk5OTU5LCJleHAiOjE2NjIwMTQzNTl9.EuZLNHqHQc7gGYFF2JHqlTuBpNQXFo11t0ZDWoOx6Ys',
  'language': 'en'
}

with open('./withdraw_busd.json', 'w') as the_file:
    for _ in range(0, 100000, 200):
        url = "https://www.x-meta.com/bc/v1/exchange/spot-withdraw-record?startTime=1659196800000&endTime=1661961599000&status=10&asset=BUSD&offset={}&limit=200".format(_)
        response = requests.request("GET", url, headers=headers)
        data = response.json()
        
        try:
            assert data['code'] == 0
        except:
            sleep(10)
            response = requests.request("GET", url, headers=headers)

        if len(data["data"]["spotWithdrawRecord"]) == 0:
            the_file.write(json.dumps(data_best))
            print(data_best)
            print('FINISHED!.')
            break

        for user in data['data']['spotWithdrawRecord']:
            if len(user['txId']) < 13 and user['asset'] not in ['IHC', 'MNTC'] and user['uid'] not in ['169586', '176570']:
                if user['asset'] in data_best.keys():
                    data_best[str(user['asset'])] += float(user['amount'])
                else:
                    data_best[str(user['asset'])] = float(user['amount'])
        
        print(f'{_} - {len(data["data"]["spotWithdrawRecord"])}')
    