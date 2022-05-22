from privateconfig import p_api_key, p_secret_key
from datetime import datetime
import requests
import json
import hmac
import hashlib
import base64
from urllib.parse import urlencode
import pandas as pd

def generate_sign(method, base_uri, endpoint, params, secret_key):
    '''
    Generate a request signature for a given method, endpoint, params and secret key.
    '''
    pre_signed_text = method + '\n' + base_uri + '\n' + endpoint + '\n' + params
    hash_code = hmac.new(p_secret_key.encode(), pre_signed_text.encode(), hashlib.sha256).digest()
    signature = urlencode({'Signature': base64.b64encode(hash_code).decode()})

    return signature

base_uri = 'api-aws.huobi.pro'

rums = []
for symbol in ['btcusdt', 'ethusdt', 'bnbusdt', 'htusdt']:
    timestamp = str(datetime.utcnow().isoformat())[0:19]
    params = urlencode({'AccessKeyId': p_api_key,
                    'SignatureMethod': 'HmacSHA256',
                    'SignatureVersion': '2',
                    'Timestamp': timestamp,
                    'symbol': symbol,
                    'period': '1min',
                    'size': 2
                    })
    method = 'GET'
    endpoint = '/market/history/kline'
    signature = generate_sign(method, base_uri, endpoint, params, p_secret_key)
    url = 'https://' + base_uri + endpoint + '?' + params + '&' + signature
    response = requests.request(method, url)
    resp = json.loads(response.text)

    row = []
    for r in resp['data']:
        c_time = datetime.fromtimestamp(r['id']).strftime('%Y-%m-%d %H:%M:%S')
        row.append([c_time, r['open'], r['high'], r['low'], r['close']])

    data = pd.DataFrame(row, columns=['Time', 'Open', 'High', 'Low', 'Close'])
    data['Time'] = pd.to_datetime(data['Time'])
    data.sort_values(by='Time', ascending=True, inplace=True)
    data.reset_index(drop=True, inplace=True)
    
    difference = data.iloc[-1]['Close'] - data.iloc[0]['Close']
    difference = difference / data.iloc[0]['Close'] * 100

    class_fa = ""

    if data.iloc[-1]['Close'] > data.iloc[0]['Close']:
        difference = "+" + str(round(difference, 2)) + "%"
        class_fa = "fa fa-level-up"
    elif data.iloc[-1]['Close'] < data.iloc[0]['Close']:
        difference = "-" + str(round(difference, 2)) + "%"
        class_fa = "fa fa-level-down"
    else:
        difference = "0.00%"
    
    difference = """<span class="small text-danger">{} <i class="{}"></i></span>""".format(difference, class_fa)
    print(symbol, difference, data.iloc[-1]['Close'])
    rums.append([symbol, difference, data.iloc[-1]['Close']])
    print(rums)