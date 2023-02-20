import requests
from time import sleep

headers = {
  'Authorization': f'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiZmYxNmM4MmYyMDBiNGE0M2I0YTk0ZjcxMDEwYmJjODgiLCJ0diI6MCwiaWF0IjoxNjcyNjIzNTc4LCJleHAiOjE2NzI2Mzc5Nzh9.r2eeUjg3WOHNpgKgs-kko--nJXFjep7kmB4aKuvMJf0',
  'language': 'en'
}


with open('./lastIndex.csv', 'r') as the_file:
    line = the_file.readline()
    last_line = int(line.strip())
    print(f'READ LAST ROW INDEX: {last_line}')

with open('./user_ids.csv', 'r') as the_file:
        lines = the_file.readlines()
        for line in lines[last_line:]:
            try:
                try:
                    url = "https://www.x-meta.com/bc/v1/exchange/customer/asset?uid={}".format(line.strip())
                    response = requests.request("GET", url, headers=headers)
                    data = response.json()
                    assert data['code'] == 0
                    last_line += 1
                except:
                    sleep(15)
                    response = requests.request("GET", url, headers=headers)
                    data = response.json()
                    if data['code'] == 0:
                        last_line += 1
                    else:
                        print(f'ERROR: {line.strip()}, {data}')
                        with open('./lastIndex.csv', 'w') as the_file:
                            text = f'Last Row: {last_line}'
                            print(text)
                            the_file.write(f'{last_line}')
                            break
                
                with open('./user_balance.csv', 'a') as balance_file:
                    for asset in data['data']['assetList']:
                        text = f'{line.strip()},{asset["asset"]},{float(asset["free"]) + float(asset["locked"])}'
                        balance_file.write('{}\n'.format(text))
                    print(line.strip())

            except:
                with open('./lastIndex.csv', 'w') as the_file:
                    text = f'Last Row: {last_line}'
                    print(text)
                    the_file.write(f'{last_line}')
