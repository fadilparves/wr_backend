from datetime import datetime
import requests
import json
import hmac
import hashlib
import base64
from urllib.parse import urlencode
from privateconfig import p_api_key, p_secret_key
import pandas as pd
import random
import math

def generate_sign(method, base_uri, endpoint, secret_key):
    '''
    Generate a request signature for a given method, endpoint, params and secret key.
    '''
    pre_signed_text = method + '\n' + base_uri + '\n' + endpoint + '\n' + params
    hash_code = hmac.new(p_secret_key.encode(), pre_signed_text.encode(), hashlib.sha256).digest()
    signature = urlencode({'Signature': base64.b64encode(hash_code).decode()})

    return signature

#Get all Accounts of the Current User

base_uri = 'api-aws.huobi.pro'
# account_balance = 0

method = 'GET'
endpoint = '/v1/account/accounts'
timestamp = str(datetime.utcnow().isoformat())[0:19]
params = urlencode({'AccessKeyId': p_api_key,
                'SignatureMethod': 'HmacSHA256',
                'SignatureVersion': '2',
                'Timestamp': timestamp
                })

signature = generate_sign(method, base_uri, endpoint, p_secret_key)
url = 'https://' + base_uri + endpoint + '?' + params + '&' + signature
response = requests.request(method, url)
accts = json.loads(response.text)
account_id = accts['data'][0]['id']
print(account_id)