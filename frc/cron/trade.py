from sys import flags
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


def trade():
    meta_data = get_token_and_rate(given_date)
    header = 'uid,symbol,price,mnt_price,busd_amount,mnt_amount,token_amount,type,createTime,wallet'
    busd_rate = float(meta_data['rate'])

    headers = {
        'Authorization': f'Bearer {meta_data["token"]}',
        'language': 'en'
    }

    with open('./trade_{}.csv'.format(given_date), 'a') as the_file:
        the_file.write('{}\n'.format(header))
        
        for _ in range(0, 1000000, 500):
            url = "https://www.x-meta.com/bc/v1/exchange/trade-records?startTime={}&endTime={}&settleStatus=10&offset={}&limit=500".format(
                yesterday_date_range, today_date_range, _)
            response = requests.request("GET", url, headers=headers)

            data = response.json()

            try:
                assert data['code'] == 0
            except:
                sleep(15)
                meta_data = get_token_and_rate(given_date)
                headers = {
                    'Authorization': f'Bearer {meta_data["token"]}',
                    'language': 'en'
                }
                response = requests.request("GET", url, headers=headers)
            
            if len(data["data"]["tradeRecords"]) == 0:
                print('finished!.')
                break

            for trade in data['data']['tradeRecords']:
                crtObj = datetime.fromtimestamp(int(trade['createTime']) // 1000)
                createdDate = crtObj.strftime('%Y-%m-%d-%H-%M')

                updateObj = datetime.fromtimestamp(int(trade['updateTime']) // 1000)
                updatedDate = updateObj.strftime('%Y-%m-%d-%H-%M')

                price = float(trade['price'])
                amount_busd = float(trade['quoteQty'])
                token_amount = float(trade['qty'])

                mnt_price = math.ceil((price * busd_rate) * 100) / 100
                mnt_amount = math.ceil((amount_busd * busd_rate) * 100) / 100
                wallet = 'n/a'
                
                if mnt_amount >= 20000000:
                    url = "https://www.x-meta.com/bc/v1/exchange/customer/asset?uid={}".format(trade['uid'])
                    response = requests.request("GET", url, headers=headers)
                    wallet_data = response.json()
                    if wallet_data['code'] == 0:
                        for wal_addr in wallet_data['data']['depositList']:
                            if wal_addr['asset'] == 'BUSD':
                                wallet = wal_addr['address']

                    row = f"{trade['uid']},{trade['symbol']},{price},{mnt_price},{amount_busd},{mnt_amount},{token_amount},{trade['tradeDirection']},{createdDate},{wallet}\n"
                    the_file.write(row)
            print(f'{_} - {len(data["data"]["tradeRecords"])}')


if __name__ == "__main__":
    main()
