from itertools import tee
import requests
from time import sleep

header = 'id'

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiZTllYzFhMGUxN2U4NDVjM2FjYmQ1YzcxYmY5MTlmOTEiLCJ0diI6MCwiaWF0IjoxNjYxMzk2NzgxLCJleHAiOjE2NjE0MTExODF9.snZ6-VMonEtoqjlAiXOGy7_tupVlyXKc-qe4GIDiaeE',
  'language': 'en'
}

sum_num = 0

with open('./operate.csv', 'r') as the_file:
    the_file.readline()
    lines = the_file.readlines()
    for line in lines:
            # try:
            #     url = "https://www.x-meta.com/bc/v1/exchange/customers?keyword={}&offset=0&limit=100".format(line.strip())
            #     response = requests.request("GET", url, headers=headers)
            #     data = response.json()
            #     assert data['code'] == 0
            # except:
            #     sleep(15)
            #     response = requests.request("GET", url, headers=headers)

            # if data['code'] != 0:
            #     print(f'ERROR: {line.strip()}, {data}')
            #     break

            # with open('./email_with_userId.csv', 'a') as the_file:
            #     for user in data['data']['userList']:
            #         text = f'{line.strip()},{user["uid"]}\n'
            #         print(text)
            #         the_file.write('{}\n'.format(text))
        num = float(line.split(',')[5])
        sum_num += num

print(sum_num)
