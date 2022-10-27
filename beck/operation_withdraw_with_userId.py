import requests
from time import sleep
from datetime import datetime


header = 'asset,amount,createDate,uid,txId'

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiNzU3Yzc5ZWQ3MzlhNGZkMzk4OTJiMjU5ZGUyN2JhNzAiLCJ0diI6MCwiaWF0IjoxNjY2MzQxNTkyLCJleHAiOjE2NjYzNTU5OTJ9.TLuEcCYLpk16yi1I5C2N2cXYFEUCFYkk9Eh5IcYlMyU',
  'language': 'en'
}

with open('./july_withdraw_with_userID.csv', 'a') as the_file:
    the_file.write('{}\n'.format(header))
    for _ in range(0, 1000000, 200):
        url = "https://www.x-meta.com/bc/v1/exchange/spot-withdraw-record?keyword=operation@x-meta.com&startTime=1656604800000&endTime=1659283200000&status=10&asset=BUSD&offset={}&limit=200".format(_)
        response = requests.request("GET", url, headers=headers)
        data = response.json()
        
        try:
            assert data['code'] == 0
        except:
            sleep(10)
            response = requests.request("GET", url, headers=headers)

        if len(data["data"]["spotWithdrawRecord"]) == 0:
            break

        for user in data['data']['spotWithdrawRecord']:
            crtObj = datetime.fromtimestamp(int(user['createTime']) // 1000)
            createdDate = crtObj.strftime('%Y-%m-%d')
            tx_id = user['txId']

            url = "https://www.x-meta.com/bc/v1/exchange/spot-deposit-record?txId={}&offset=0&limit=100".format(tx_id)
            response = requests.request("GET", url, headers=headers)
            data_detail = response.json()

            try:
                assert data_detail['code'] == 0
            except:
                sleep(15)
                response = requests.request("GET", url, headers=headers)
                data_detail = data_detail = response.json()

            try:
                uid = data_detail['data']['spotDepositRecord'][0]['uid']
            except KeyError as err:
                print(err)
                uid = 'n/a'

            if uid == '175427':
                print('{},{},{},{},{}\n'.format(user['asset'], user['amount'], createdDate, uid, tx_id))
                continue

            the_file.write('{},{},{},{},{}\n'.format(user['asset'], user['amount'], createdDate, uid, tx_id))
        print(f'{_} - {len(data["data"]["spotWithdrawRecord"])}')
