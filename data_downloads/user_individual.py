import requests
from time import sleep

header = 'uid,name,phone'

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiYmJhZDY0Njc4MDhmNGEzNmEzZmM0MDE1ZmFhMzAzNDgiLCJ0diI6MCwiaWF0IjoxNjc2NDQ0NjA0LCJleHAiOjE2NzY0NTkwMDR9.0FuQX8zWtu8s4J6PQIEBC0aefoErx6Z_IoE06gceBh8',
  'language': 'en'
}


with open('./ids.csv', 'r') as the_file:
    with open('./3000-data.csv', 'a') as write_file:

        lines = the_file.readlines()
        for line in lines:
            
            try:
                url = "https://www.x-meta.com/bc/v1/exchange/customers?keyword={}&offset=0&limit=100".format(line.strip())
                response = requests.request("GET", url, headers=headers)
                data = response.json()
                assert data['code'] == 0
            except:
                sleep(15)
                response = requests.request("GET", url, headers=headers)
            
            text = f'{line.strip()},{data["data"]["userList"][0]["name"]},{data["data"]["userList"][0]["phone"]}'
            print(text)
            write_file.write('{}\n'.format(text))
