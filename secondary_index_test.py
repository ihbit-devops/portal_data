import datetime
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
record_table = dynamodb.Table('bank_deposit')



def is_user_daily_limit_exceeded(email, amount):
    utc_time = datetime.datetime.utcnow()
    ub_time_difference = datetime.timedelta(hours=8)
    ub_time = utc_time + ub_time_difference
    today = ub_time.strftime("%Y-%m-%d")

    response = record_table.query(
        IndexName='description-createdDate-index',
        ScanIndexForward=True,
        KeyConditionExpression=Key('description').eq(email)
    )

    total_db = 0
    for item in response.get('Items'):
        if item['postDate'] == today:
            if item['status'] == '2.5' or item['status'] == '3':
                total_db += float(item['amount'])
    check = total_db + float(amount)
    
    print('INFO: Input Amount:{}, Today DB amount:{}, Total amount:{}, Email: {}'.format(amount, total_db, check, email))
    
    return True if check > 20000000.0 else False



print(is_user_daily_limit_exceeded('eruulteruult69@gmail.com', 0))