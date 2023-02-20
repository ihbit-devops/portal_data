import requests
from time import sleep

header = 'uid,name,phone'

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiYmJhZDY0Njc4MDhmNGEzNmEzZmM0MDE1ZmFhMzAzNDgiLCJ0diI6MCwiaWF0IjoxNjc2NDQ0NjA0LCJleHAiOjE2NzY0NTkwMDR9.0FuQX8zWtu8s4J6PQIEBC0aefoErx6Z_IoE06gceBh8',
  'language': 'en'
}


with open('./tuvshin_final.csv', 'r') as the_file:
    with open('./formated_sheet_final.csv', 'a') as write_file:
        data = {}
        lines = the_file.readlines()
        last_date = ''
        for line in lines:
            
            # try:
            #     url = "https://www.x-meta.com/bc/v1/exchange/customers?keyword={}&offset=0&limit=100".format(line.strip())
            #     response = requests.request("GET", url, headers=headers)
            #     data = response.json()
            #     assert data['code'] == 0
            # except:
            #     sleep(15)
            #     response = requests.request("GET", url, headers=headers)
            
            # text = f'{line.strip()},{data["data"]["userList"][0]["name"]},{data["data"]["userList"][0]["phone"]}'
            # print(text)
            # write_file.write('{}\n'.format(text))
            date_field = line.split(',')[0]
            if '2022-' in date_field or '2023-' in date_field:
                last_date = date_field
                data[last_date] = []
            else:
                data[last_date].append(line)

        for k in data.keys():
            for item in data[k]:
                uid = item.split(',')[0].strip()
                count = item.split(',')[1].strip()
                sum = item.split(',')[2].strip()
                price = item.split(',')[3].strip()
                
                if int(count) >= 2:
                    text = f'{uid},{count},{sum},{price},{k}'
                    write_file.write('{}\n'.format(text))

