import requests
from time import sleep
from datetime import datetime
import math


header = 'uid,amount,mnt_amount,rate,createDate,wallet,txId'
busd_rate = 3485
given_date = '11-16'

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiMDUzYzEzNWZmYTg4NGZiNDg0ODIyYjg1YjIzY2FiODkiLCJ0diI6MCwiaWF0IjoxNjY1OTk2MTU1LCJleHAiOjE2NjYwMTA1NTV9.mxQ0R4OS4iqDq9pn6sDBt6xKdMCvPg3V0x9EcnamJHM',
  'language': 'en'
}

with open('./bank_deposit_{}.csv'.format(given_date), 'a') as the_file:
    the_file.write('{}\n'.format(header))
    for _ in range(0, 1000000, 200):
        url = "https://www.x-meta.com/bc/v1/exchange/spot-withdraw-record?keyword=operation@x-meta.com&startTime=1665417600000&endTime=1665936000000&status=10&asset=BUSD&offset={}&limit=200".format(_)
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
            createdDate = crtObj.strftime('%Y-%m-%d-%H-%M')

            data_detail = response.json()

            try:
                assert data_detail['code'] == 0
            except:
                sleep(15)
                response = requests.request("GET", url, headers=headers)
                data_detail = data_detail = response.json()

            amount = float(user['amount'])
            mnt_amount = math.ceil((amount * busd_rate) * 100) / 100

            if mnt_amount >= 20000000:
                url = "https://www.x-meta.com/bc/v1/exchange/spot-deposit-record?txId={}&offset=0&limit=100".format(user['txId'])
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
                the_file.write('{},{},{},{},{},{},{}\n'.format(uid, amount, mnt_amount, busd_rate, createdDate, user['address'], user['txId']))

        print(f'{_} - {len(data["data"]["spotWithdrawRecord"])}')
