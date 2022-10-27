from calendar import day_abbr
import datetime
import json

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
record_table = dynamodb.Table('bank_deposit')

utc_time = datetime.datetime.utcnow()
ub_time_difference = datetime.timedelta(hours=8)
ub_time = utc_time + ub_time_difference
today = ub_time.strftime("%Y-%m-%d")

uid_with_emails = None
with open('./uidsWithEmail.json', 'r') as f:
    uid_with_emails = json.loads(f.readline())


with open('/Users/devops/Downloads/july-deposit-uid.csv', 'a') as depo_f:
    for idx in range(1, 32):
        day = idx

        if idx < 10:
            day = f'0{idx}'
        
        response = record_table.query(
            IndexName='postDate-createdDate-index-report',
            ScanIndexForward=True,
            KeyConditionExpression=Key('postDate').eq('2022-07-{}'.format(day))
        )

        for item in response.get('Items'):
            if item['status'] == '3':
                line = dict(item)

                try:
                    line['description'] = uid_with_emails[line['description']]
                except:
                    print('None!.')
                    line['description'] = 'N/A'
                    continue

                depo_f.write(f'{line["description"]},{line["id"]},{line["postDate"]},{line["amount"]},{line["createdDate"]},{line["status"]}\n')
        print(f'{day} -> {len(response.get("Items"))}')
