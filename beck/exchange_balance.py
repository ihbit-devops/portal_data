import requests
from time import sleep
from datetime import datetime


header = 'asset,amount,date'
headers = {
  'Authorization': f'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiMWJkNDRmZDJmZmY0NDJjMDhiM2M0YmJjZDFiNzQ5ZTUiLCJ0diI6MCwiaWF0IjoxNjc2MDI0NTc1LCJleHAiOjE2NzYwMzg5NzV9.1wNcJV53MnFx0YNnBzc_bN4cY_CG__4l9OT5UV3oHPQ',
  'language': 'en'
}


with open('./jan_balance.csv', 'a') as the_file:
    the_file.write('{}\n'.format(header))
    url = "https://www.x-meta.com/bc/v1/exchange/account/asset-statistics?startTime=1675094400000&endTime=1675180800000"
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    
    try:
        assert data['code'] == 0
    except:
        sleep(10)
        response = requests.request("GET", url, headers=headers)

    for asset in data['data']['assetStatistics']:
        the_file.write('{},{},{}\n'.format(asset['asset'], asset['totalAmount'], asset['executeDate']))      
