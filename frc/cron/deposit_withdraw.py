from time import sleep
from datetime import datetime, timedelta
import math

import requests
import boto3


today_date_obj = datetime.now()
yesterday_date_obj = today_date_obj - timedelta(1)
given_date = datetime.strftime(yesterday_date_obj, '%Y-%m-%d')

yesterday_date_range = int(datetime(yesterday_date_obj.year, yesterday_date_obj.month, 
                            yesterday_date_obj.day).timestamp() * 1000)
today_date_range = int(datetime(today_date_obj.year, today_date_obj.month, 
                            today_date_obj.day).timestamp() * 1000)

dynamo = boto3.client('dynamodb')
ssm = boto3.client('ssm')


def get_token_and_rate(date_to_fetch):
    rate = dynamo.get_item(
        Key={
            'date': {
                'S': date_to_fetch,
            }
        },
        ReturnConsumedCapacity='TOTAL',
        TableName='mongol_bank_rate'
    )['Item']['value']['S']

    token = ssm.get_parameter(Name='/portal/token', WithDecryption=True)['Parameter']['Value']

    return {
        'rate': rate,
        'token': token
    }


def main():
    meta_data = get_token_and_rate(given_date)
    header = 'uid,asset,price,mnt_price,amount,mnt_amount,network,address,createDate,finishDate'
    busd_rate = float(meta_data['rate'])

    prices = {
        'BUSD': 1,
        'USDT': 1
    }

    headers = {
    'Authorization': f'Bearer {meta_data["token"]}',
    'language': 'en'
    }

    print('-------------------------------Deposit--------------------------------------')
    with open('./deposit_{}.csv'.format(given_date), 'a') as the_file:
        the_file.write('{}\n'.format(header))
        for _ in range(0, 100000, 200):
            url = "https://www.x-meta.com/bc/v1/exchange/spot-deposit-record?startTime={}&endTime={}&status=10&offset={}&limit=200".format(
                        yesterday_date_range, today_date_range, _)
            response = requests.request("GET", url, headers=headers)
            data = response.json()
            
            try:
                assert data['code'] == 0
            except:
                sleep(10)
                response = requests.request("GET", url, headers=headers)

            if len(data["data"]["spotDepositRecord"]) == 0:
                break

            for deposit in data['data']['spotDepositRecord']:
                crt_obj = datetime.fromtimestamp(int(deposit['createTime']) // 1000)
                created_date = crt_obj.strftime('%Y.%m.%d')

                fns_obj = datetime.fromtimestamp(int(deposit['finishTime']) // 1000)
                finish_date = fns_obj.strftime('%Y.%m.%d')


                if deposit['asset'] not in prices:
                    url = "https://www.x-meta.com/open/v1/market/depth?symbol={}_BUSD&limit=10".format(deposit['asset'])
                    response = requests.request("GET", url, headers=headers)
                    price_data = response.json()
                    
                    if price_data['code'] != 0:
                        prices[deposit['asset']] = 0
                    else:
                        asset_current_price_busd = price_data['data']['asks'][0][0]
                        prices[deposit['asset']] = float(asset_current_price_busd)
                
                mnt_price = math.ceil((prices[deposit['asset']] * busd_rate) * 100) / 100
                mnt_value = math.ceil(float(deposit['amount']) * mnt_price)

                if mnt_value >= 20000000:
                    the_file.write('{},{},{},{},{},{},{},{},{},{}\n'.format(deposit['uid'], deposit['asset'], prices[deposit['asset']], 
                        mnt_price, deposit['amount'], mnt_value, deposit['network'], deposit['address'], created_date, finish_date))
            
            print(f'{_} - {len(data["data"]["spotDepositRecord"])}')

    print('-------------------------------Withdraw--------------------------------------')

    with open('./withdraw_{}.csv'.format(given_date), 'a') as the_file:
        the_file.write('{}\n'.format(header))
        for _ in range(0, 100000, 200):
            url = "https://www.x-meta.com/bc/v1/exchange/spot-withdraw-record?startTime={}&endTime={}&status=10&offset={}&limit=200".format(
                    yesterday_date_range, today_date_range ,_)
            response = requests.request("GET", url, headers=headers)
            data = response.json()
            
            try:
                assert data['code'] == 0
            except:
                sleep(10)
                response = requests.request("GET", url, headers=headers)

            if len(data["data"]["spotWithdrawRecord"]) == 0:
                break

            for withdraw in data['data']['spotWithdrawRecord']:
                crt_obj = datetime.fromtimestamp(int(withdraw['createTime']) // 1000)
                created_date = crt_obj.strftime('%Y.%m.%d')

                fns_obj = datetime.fromtimestamp(int(withdraw['finishTime']) // 1000)
                finish_date = fns_obj.strftime('%Y.%m.%d')

                if withdraw['uid'] == "176570" or withdraw['uid'] == "169586":
                    continue

                if withdraw['asset'] not in prices:
                    url = "https://www.x-meta.com/open/v1/market/depth?symbol={}_BUSD&limit=10".format(withdraw['asset'])
                    response = requests.request("GET", url, headers=headers)
                    price_data = response.json()
                    
                    if price_data['code'] != 0:
                        prices[withdraw['asset']] = 0
                    else:
                        asset_current_price_busd = price_data['data']['asks'][0][0]
                        prices[withdraw['asset']] = float(asset_current_price_busd)
                
                mnt_price = math.ceil((prices[withdraw['asset']] * busd_rate) * 100) / 100
                mnt_value = math.ceil(float(withdraw['amount']) * mnt_price)

                if mnt_value >= 20000000:
                    the_file.write('{},{},{},{},{},{},{},{},{},{}\n'.format(withdraw['uid'], withdraw['asset'], prices[withdraw['asset']], 
                        mnt_price, withdraw['amount'], mnt_value, withdraw['network'], withdraw['address'], created_date, finish_date))
            
            print(f'{_} - {len(data["data"]["spotWithdrawRecord"])}')



if __name__ == "__main__":
    main()
