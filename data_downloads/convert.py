import os
import json
import math

import boto3

ssm = boto3.client('ssm')
BUSD_RATE_PARAMETER_NAME = os.environ['BUSD_RATE_PARAMETER_NAME']


def lambda_handler(event, context):
    """ Converting incoming asset into MNT """
    
    from_asset = event.get('from', None)
    amount = event.get('amount', None)
    
    if from_asset is None or from_asset != 'BUSD':
        return {
            'statusCode': 400,
            'msg': 'Not supported convertion!.'
        }
    
    if amount is None:
        return {
            'statusCode': 400,
            'msg': 'Amount must be specified in the body!..'
        }
        
    # Getting ask
    response = ssm.get_parameter(
        Name=BUSD_RATE_PARAMETER_NAME, WithDecryption=True)
    ask = response['Parameter']['Value'].split('-')[1]
    
    try:
        mnt_amount = float(amount) * float(ask)
        mnt_amount = math.ceil(mnt_amount * 1000) /1000.0
        
        return {
            'statusCode': 200,
            'BUSD': amount,
            'MNT': mnt_amount
        }
        
    except Exception as e:
        return {
            'statusCode': 400,
            'msg': 'Amount must be specified in the body!..'
        }
        console.log('ERROR: Had problem with converting!.')
        console.log(e)
        raise e
    
    
