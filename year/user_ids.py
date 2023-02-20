import requests
from time import sleep

header = 'id,name'

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiNzQxNzc2YWExZDVjNDhhYzlhNTVmNTg5NjA4MzJhMDUiLCJ0diI6MCwiaWF0IjoxNjc0MTE5MDA5LCJleHAiOjE2NzQxMzM0MDl9.C_1a_vtMraxZrEpH8IcH8KFPyC_dYx0lNBUKvKzvzn4',
  'language': 'en'
}


with open('./users.csv', 'a') as the_file:
    for _ in range(0, 75000, 200):
        url = "https://www.x-meta.com/bc/v1/exchange/customers?startTime=1640966400000&endTime=1672502400000&status=1&offset={}&limit=200".format(_)
        response = requests.request("GET", url, headers=headers)
        data = response.json()

        try:
            assert data['code'] == 0
        except:
            sleep(15)
            response = requests.request("GET", url, headers=headers)
        
        if len(data["data"]["userList"]) == 0:
            break

        for user in data['data']['userList']:
            if user['name'] == '':
                continue
            
            row = f"{user['uid']},{user['name']}\n"
            the_file.write(row)

        print(f'{_} - {len(data["data"]["userList"])}')
