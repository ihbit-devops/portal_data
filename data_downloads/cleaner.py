import json
import uuid
import os
import re
import datetime

import boto3

sqs = boto3.resource('sqs')
sqs_client = boto3.client('sqs')
dynamo = boto3.client('dynamodb')

BANK_DEPOSIT_TABLE_NAME = os.environ[
                'BANK_DEPOSIT_TABLE_NAME']
BANK_DESCRIPTION_CLEANER_QUEUE_NAME = os.environ[
                'BANK_DESCRIPTION_CLEANER_QUEUE_NAME']
BANK_DEPOSIT_QUEUE_URL = os.environ['BANK_DEPOSIT_QUEUE_URL']
USER_INFO_TABLE_NAME = os.environ['USER_INFO_TABLE_NAME']

record_table = boto3.resource('dynamodb').Table(BANK_DEPOSIT_TABLE_NAME)
queue = sqs.get_queue_by_name(QueueName=BANK_DESCRIPTION_CLEANER_QUEUE_NAME)


def lambda_handler(event, context):
    
    # Receive messages from SQS queue
    queue_group_id = str(uuid.uuid1())

    print("ApproximateNumberOfMessages:",
          queue.attributes.get('ApproximateNumberOfMessages'))

    for message in queue.receive_messages(MaxNumberOfMessages=10):
        cleaning_message = json.loads(message.body)

        unique_id = cleaning_message.get('uniqueId')
        desc = cleaning_message.get('description')
        related_acc = cleaning_message.get('relatedAccount')
        journal = cleaning_message.get('journal')
        amount = cleaning_message.get('amount')
        
        # Getting email
        email = description_clean(desc)
        print('INFO: Cleaned description!. desc: {} ---> email: {}'.format(desc, email))
        
        #TEMP------------
        #Avoid 20mil abuse
        
        if is_user_daily_limit_exceeded(email, amount) and email != '':
            response = record_table.update_item(
                Key={
                    'id': unique_id,
                    'journal': journal
                },
                UpdateExpression="set #status=:s",
                ExpressionAttributeNames={
                    '#status': 'status',
                },
                ExpressionAttributeValues={
                    ':s': '10'
                },
                ReturnValues="UPDATED_NEW"
            )
            print('ALERT: 20 MILLIONS ABUSE!!!!!!!!!!!!!!!!!.')
            message.delete()
            return
        
        else:
            # Desc is None
            if email == '':
                # Clear record description, If description is empty status: 5
                # Update record status to 5
                response = record_table.update_item(
                    Key={
                        'id': unique_id,
                        'journal': journal
                    },
                    UpdateExpression="set #status=:s",
                    ExpressionAttributeNames={
                        '#status': 'status',
                    },
                    ExpressionAttributeValues={
                        ':s': '5'
                    },
                    ReturnValues="UPDATED_NEW"
                )
                print('INFO: Updated status to 5, desc is empty.!')
                
                
            else:
                # Find user wallet and return it!.
                wallet = get_user_wallet(email)
                print("INFO: Tried to get wallet!.")
                
                if wallet is None:
                    # Update record status to 6, 6 is user not found
                    response = record_table.update_item(
                        Key={
                            'id': unique_id,
                            'journal': journal
                        },
                        UpdateExpression="set #status=:s",
                        ExpressionAttributeNames={
                            '#status': 'status',
                        },
                        ExpressionAttributeValues={
                            ':s': '6'
                        },
                        ReturnValues="UPDATED_NEW"
                    )
                    print('INFO: Updated status to 6, wallet not found!.')
    
                    
                else:
                    
                    # Update record status to 2
                    response = record_table.update_item(
                        Key={
                            'id': unique_id,
                            'journal': journal
                        },
                        UpdateExpression="set #status=:s, #desc=:d",
                        ExpressionAttributeNames={
                            '#status': 'status',
                            '#desc': 'description',
                        },
                        ExpressionAttributeValues={
                            ':s': '2',
                            ':d': email
                        },
                        ReturnValues="UPDATED_NEW"
                    )
                    print('INFO: Updated status to 2.!')
                    
                    # Add to deposit queue
                    deposit_message = {
                        'wallet': wallet,
                        'amount': amount,
                        'uniqueId':unique_id,
                        'journal': journal
                    }
                    
                    sqs_client.send_message(
                        QueueUrl=BANK_DEPOSIT_QUEUE_URL, 
                        MessageBody=json.dumps(deposit_message),
                        MessageDeduplicationId=unique_id,
                        MessageGroupId=queue_group_id,
                    )
                    print('INFO: Added to Deposit queue.!')
                    
        # Delete message from queue
        message.delete()

        
def description_clean(desc: str) -> str:
        # Empty description
    desc = desc.strip()
    
    if desc == '':
        return ''
    
    # Adding gmail and yahoo
    lowered_desc = desc.lower()
    if 'gmail' in lowered_desc and '@' not in lowered_desc:
        splitted_email = lowered_desc.split('gmail')
        desc = splitted_email[0] + '@gmail' + splitted_email[1]

    if 'yahoo' in lowered_desc and '@' not in lowered_desc:
        splitted_email = lowered_desc.split('yahoo')
        desc = splitted_email[0] + '@yahoo' + splitted_email[1]
    desc = desc.upper()
    
    
    replacements = {
        'EB-':'',
        'EB -':'',
        'MM:':'',
        'MM: ':'',
        '+':'',
        '*':'',
        '%':'',
        'qpay':'',
        '(ГОЛОМТБАНКИКСМЕТАХХК)':''
    }
    
    # CLeaning from outside
    for key in replacements.keys():
        if key in desc:
            desc = desc.replace(key, '')
    
    description = desc.upper()
    data_arr = description.split(' ')

    result = []
    for item in data_arr:
        if item != '':
            result.append(item)
    
    tmp = ''.join(result).strip().lower()

    email = ''
    is_found_invalid = False
    
    for index, ltr in enumerate(tmp):
       if ltr == '@':
           email += tmp[:index]
           sub_email = tmp[index:]
           
           for idx, lt in enumerate(sub_email):
                if lt == '.':
                    email += sub_email[:idx]
                    sub_sub_email = sub_email[idx:]
                    
                    for id, l in enumerate(sub_sub_email):
                        if l == '(' or l == '-' or l == '_' or l == ',':
                            email += sub_sub_email[:id]
                            is_found_invalid = True
                            break
                    if is_found_invalid == False:
                        email += sub_sub_email


    result = re.sub(r'[^\x00-\x7F\x80-\xFF\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF]', u'', email) 
    return result.strip()
     

def get_user_wallet(email):
    # Looking for wallet by email
    response = dynamo.get_item(
        Key={
            'email': {
                'S': email,
            }
        },
        ReturnConsumedCapacity='TOTAL',
        TableName='user_info',
        ProjectionExpression='wallet',
    )
    
    # If user not found!.
    if 'Item' not in response:
        return None
        
    print(response)
    print(response.get('Item').get('wallet').get('S', None))
        
    try:
        return response.get('Item').get('wallet').get('S', None)
    except AttributeError:
        print('ERROR: Had problem with fetching wallet from DB!. AWS 500')
        return None


def is_user_daily_limit_exceeded(email, amount):
    utc_time = datetime.datetime.utcnow()
    ub_time_difference = datetime.timedelta(hours=8)
    ub_time = utc_time + ub_time_difference
    
    query_date = ub_time.strftime("%Y-%m-%d")
    
    data = dynamo.scan(
        TableName='bank_deposit',
        Select = 'ALL_ATTRIBUTES',
        ScanFilter={
            'createdDate': {
                'AttributeValueList': [
                    {
                        'S': query_date,
                    },
                ],
                'ComparisonOperator': 'CONTAINS'
            },
            'description': {
                'AttributeValueList': [
                    {
                        'S': email,
                    },
                ],
                'ComparisonOperator': 'EQ'
            }
        },
    )
    
    sum = 0
    for tx in data['Items']:
        sum += float(tx['amount']['N'])
    
    sum += float(amount)
    
    return True if sum > 20000000.0 else False
    