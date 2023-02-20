from time import sleep
from datetime import datetime, timedelta
import math

import requests
import boto3


given_date = '2022-11-01'

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

    headers = {
        'Authorization': f'Bearer {meta_data["token"]}',
        'language': 'en'
    }

    with open('./oct_deposit.csv', 'a') as the_file:
        the_file.write('{}\n'.format(header))
        for _ in range(0, 100000, 200):
            url = "https://www.x-meta.com/bc/v1/exchange/spot-deposit-record?startTime=1664553600000&endTime=1667232000000&status=10&offset={}&limit=200".format(_)
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
                crtObj = datetime.fromtimestamp(int(deposit['createTime']) // 1000)
                createdDate = crtObj.strftime('%Y-%m-%d')
                day_of_week = crtObj.strftime('%A')

                if deposit['uid'] == "176570" or deposit['uid'] == "169586" or deposit['uid'] == "165055":
                    continue

                the_file.write('{},{},{}\n'.format(deposit['amount'], deposit['asset'], createdDate))
            
            print(f'{_} - {len(data["data"]["spotDepositRecord"])}')


    with open('./oct_withdraw.csv', 'a') as the_file:
        the_file.write('{}\n'.format(header))
        for _ in range(0, 10000, 200):
            url = "https://www.x-meta.com/bc/v1/exchange/spot-withdraw-record?startTime=1664553600000&endTime=1667232000000&status=10&offset={}&limit=200".format(_)
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
                createdDate = crtObj.strftime('%Y-%m-%d')
                day_of_week = crtObj.strftime('%A')

                the_file.write('{},{},{},{}\n'.format(user['amount'], user['asset'], createdDate, user['address']))
            
            print(f'{_} - {len(data["data"]["spotWithdrawRecord"])}')


if __name__ == "__main__":
    main()