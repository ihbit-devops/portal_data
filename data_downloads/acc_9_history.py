import requests
from time import sleep
from datetime import datetime


header = 'amount,createDate,createDateTime'

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjIsInNpZ24iOiI3YzliYzdkY2U4MmI0NDlkYTE0Mzk4OGI2MDRlODVlYyIsInR2IjowLCJpYXQiOjE2NjA2MzkwNjMsImV4cCI6MTY2MDY1MzQ2M30.ckP0N9xupnv6i8MxJzR9EQkFebKvWNEMru-lW8KiCt0',
  'language': 'en'
}


with open('./acc_9_mntc.csv', 'a') as the_file:
    the_file.write('{}\n'.format(header))
    for _ in range(0, 1000000, 200):
        url = "https://www.x-meta.com/bc/v1/exchange/operation/account-details?uid=9&asset=MNTC&offset={}&limit=200".format(_)
        response = requests.request("GET", url, headers=headers)
        data = response.json()
       
        try:
            assert data['code'] == 0
        except:
            sleep(10)
            response = requests.request("GET", url, headers=headers)

        if len(data["data"]["detailList"]) == 0:
            print('FINISHED')
            break

        for trade in data['data']['detailList']:
            crtObj = datetime.fromtimestamp(int(trade['createTime']) // 1000)
            createdDateTime = crtObj.strftime('%Y-%m-%d-%H-%M')
            createdDate = crtObj.strftime('%Y-%m-%d')
            row = f"{trade['amount']},{createdDate},{createdDateTime}\n"
            the_file.write(row)
        
        print(f"{_} - {len(data['data']['detailList'])}")