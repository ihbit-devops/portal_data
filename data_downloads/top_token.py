from os import nice
import requests
import json
from time import sleep
from datetime import datetime

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjI4LCJzaWduIjoiMjY4OTY0NGQ1MWQ3NDk2NWE3MjE2ZmQ1ODZjZjJmOTEiLCJ0diI6MCwiaWF0IjoxNjY3NjIwMDY2LCJleHAiOjE2Njc2MzQ0NjZ9.TyPlRhzAB_cgy90GlEnTtnu7HRHwNpY02JTDxQ4o-jg',
  'language': 'en'
}

tokens = {}
finish = False

with open('./top_tokens_1028-1104.csv', 'a') as the_file:
    for _ in range(0, 1000000, 500):
        
        url = "https://www.x-meta.com/bc/v1/exchange/trade-records?startTime=1666886400000&endTime=1667491200000&settleStatus=10&offset={}&limit=500".format(_)
        response = requests.request("GET", url, headers=headers)

        data = response.json()

        try:
            assert data['code'] == 0
            
        except:
            sleep(15)
            response = requests.request("GET", url, headers=headers)
        
        if len( data['data']['tradeRecords']) == 0:
            print('FINSHED!.')
            break

        for trade in data['data']['tradeRecords']:
            
            if trade['tradeDirection'].lower() == 'sell':
                crtObj = datetime.fromtimestamp(int(trade['createTime']) // 1000)
                createdDate = crtObj.strftime('%Y-%m-%d-%H-%M')
                iso = crtObj.isoformat()
               
                symbol = trade['symbol']
                quote_qty = trade['quoteQty']
                quantity = trade['qty']
                commission_asset = trade['commissionAsset']
                commission = trade['commission']
                
                if symbol in tokens.keys():
                    tokens[symbol]['volume_qty'] += float(quote_qty)
                    tokens[symbol]['volume_base'] += float(quantity)
                    tokens[symbol]['commision'] += float(commission)

                else:
                    tokens[symbol] = {
                        'volume_qty': float(quote_qty),
                        'volume_base': float(quantity),
                        'commision': float(commission),
                        'commision_asset': commission_asset
                    }
                    
        
        print(f'{_} - {len(data["data"]["tradeRecords"])}')


    the_file.write('symbol,volume_qty,volume_base,commision,commision_asset\n')
    for k in tokens.keys():
        the_file.write('{},{},{},{},{}\n'.format(k, tokens[k]['volume_qty'], tokens[k]['volume_base'], tokens[k]['commision'], tokens[k]['commision_asset']))
