from privateconfig import p_api_key, p_secret_key
from ms import market_structure
from datetime import datetime
import requests
import json
import hmac
import hashlib
import base64
from urllib.parse import urlencode
import pandas as pd
import pytz
import math
import random
from dbconn import connect

def generate_sign(method, base_uri, endpoint, params, secret_key):
    '''
    Generate a request signature for a given method, endpoint, params and secret key.
    '''
    pre_signed_text = method + '\n' + base_uri + '\n' + endpoint + '\n' + params
    hash_code = hmac.new(p_secret_key.encode(), pre_signed_text.encode(), hashlib.sha256).digest()
    signature = urlencode({'Signature': base64.b64encode(hash_code).decode()})

    return signature

def update_ms(tf, stf, ttf):
    print(tf, stf, ttf, datetime.now(pytz.timezone('Asia/Kuala_Lumpur')))
    conn = connect()
    base_uri = 'api-aws.huobi.pro'
    mkt_skt = pd.read_sql(""" select * from {} """.format(stf))
    rows_data = []
    for _, mkt in mkt_skt.iterrows():
        symbol = mkt['Symbol']
        coin = mkt['Coin']
        name = mkt['Name']
        tap = mkt['PCoin']
        tpp = mkt['PPrice']
        try:
            timestamp = str(datetime.utcnow().isoformat())[0:19]
            params = urlencode({'AccessKeyId': p_api_key,
                            'SignatureMethod': 'HmacSHA256',
                            'SignatureVersion': '2',
                            'Timestamp': timestamp,
                            'symbol': symbol,
                            'period': tf,
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
            data['Time'] = data['Time'].astype('str')
            data['Open'] = data['Open'].shift(1)
            data['High'] = data['High'].shift(1)
            data['Low'] = data['Low'].shift(1)
            data['Close'] = data['Close'].shift(1)
            data.dropna(inplace=True)
            data.reset_index(drop=True, inplace=True)
            # print(data)

            if len(data) > 0:
                symbol, ms_trend, c_buy, c_sell, wave_count_up, wave_count_down, wave_count_up_after_d, wave_count_down_after_d, upper, lower, \
                a_up, a_down, b_up, b_down, c_up, c_down, d_up, d_down, ms_buy, ms_sell, \
                laststate, last_a_price_after_d, downprice, upprice = market_structure(False, mkt['Symbol'], 
                                                                        data[-1:], mkt[ttf], mkt['CBuy'], 
                                                                        mkt['CSell'], mkt['WaveCountUp'], 
                                                                        mkt['WaveCountDown'], mkt['WaveCountUpAfterD'],
                                                                        mkt['WaveCountDownAfterD'], mkt['Upper'], 
                                                                        mkt['Lower'], mkt['AUp'], mkt['ADown'], 
                                                                        mkt['BUp'], mkt['BDown'], mkt['CUp'], 
                                                                        mkt['CDown'], mkt['DUp'], mkt['DDown'], 
                                                                        mkt['MSBuy'], mkt['MSSell'], 
                                                                        mkt['LastState'], mkt['LastAPriceAfterD'],
                                                                        mkt['DownPrice'], mkt['UpPrice'])

                rows_data.append([coin, name, symbol, tap, tpp, ms_trend, c_buy, c_sell, wave_count_up, wave_count_down, wave_count_up_after_d, wave_count_down_after_d, 
                            upper, lower, a_up, a_down, b_up, b_down, c_up, c_down, d_up, d_down, ms_buy, ms_sell, laststate, last_a_price_after_d,
                            downprice, upprice, data.iloc[-1]['Close']])
            else:
                rows_data.append([coin, name, symbol, tap, tpp, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, False, False, 0, 0.0, 0.0, 0.0, 0.0])

        except Exception as e:
            print(e)
            continue
    
    df = pd.DataFrame(rows_data, columns=['Coin', 'Name', 'Symbol', 'PCoin', 'PPrice', '{}'.format(ttf), 'CBuy', 'CSell', 'WaveCountUp', 'WaveCountDown', 'WaveCountUpAfterD', 'WaveCountDownAfterD', 
                                'Upper', 'Lower', 'AUp', 'ADown', 'BUp', 'BDown', 'CUp', 'CDown', 'DUp', 'DDown', 'MSBuy', 'MSSell', 
                                'LastState', 'LastAPriceAfterD', 'DownPrice', 'UpPrice', 'LPrice'])

    # df.to_csv("./data/{}.csv".format(stf), index=False)
    df.to_sql(stf, if_exists='replace', con=conn, index=False)