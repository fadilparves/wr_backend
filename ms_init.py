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

def generate_sign(method, base_uri, endpoint, params, secret_key):
    '''
    Generate a request signature for a given method, endpoint, params and secret key.
    '''
    pre_signed_text = method + '\n' + base_uri + '\n' + endpoint + '\n' + params
    hash_code = hmac.new(p_secret_key.encode(), pre_signed_text.encode(), hashlib.sha256).digest()
    signature = urlencode({'Signature': base64.b64encode(hash_code).decode()})

    return signature

base_uri = 'api-aws.huobi.pro'
timestamp = str(datetime.utcnow().isoformat())[0:19]
params = urlencode({'AccessKeyId': p_api_key,
                'SignatureMethod': 'HmacSHA256',
                'SignatureVersion': '2',
                'Timestamp': timestamp
                })
method = 'GET'
endpoint = '/v2/settings/common/symbols'
signature = generate_sign(method, base_uri, endpoint, params, p_secret_key)
url = 'https://' + base_uri + endpoint + '?' + params + '&' + signature
response = requests.request(method, url)
resp = json.loads(response.text)

min1 = []
min5 = []
min15 = []
h1 = []
h4 = []
d1 = []
for r in resp['data']:
    if 'sc' in r:
        if "usdt" in r['sc']:
            symbol = r['sc']
            tap = r['tap']
            tpp = r['tpp']
            coin = r['bcdn']
            name = r['dn']
            print("Symbol: {}".format(symbol))
            # 1 minute part
            try:
                timestamp = str(datetime.utcnow().isoformat())[0:19]
                params = urlencode({'AccessKeyId': p_api_key,
                                'SignatureMethod': 'HmacSHA256',
                                'SignatureVersion': '2',
                                'Timestamp': timestamp,
                                'symbol': symbol,
                                'period': '1min',
                                'size': 200
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
                    laststate, last_a_price_after_d, downprice, upprice = market_structure(True, symbol, data, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                                                    0, 0, False, False, 0, 0.0, 0.0, 0.0)

                    min1.append([coin, name, symbol, tap, tpp, ms_trend, c_buy, c_sell, wave_count_up, wave_count_down, wave_count_up_after_d, wave_count_down_after_d, 
                                upper, lower, a_up, a_down, b_up, b_down, c_up, c_down, d_up, d_down, ms_buy, ms_sell, laststate, last_a_price_after_d,
                                downprice, upprice])
                else:
                    min1.append([coin, name, symbol, tap, tpp, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, False, False, 0, 0.0, 0.0, 0.0])

            except Exception as e:
                print(e)
                continue

            # 5 minute part
            try:
                timestamp = str(datetime.utcnow().isoformat())[0:19]
                params = urlencode({'AccessKeyId': p_api_key,
                                'SignatureMethod': 'HmacSHA256',
                                'SignatureVersion': '2',
                                'Timestamp': timestamp,
                                'symbol': symbol,
                                'period': '5min',
                                'size': 200
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
                    laststate, last_a_price_after_d, downprice, upprice = market_structure(True, symbol, data, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                                                    0, 0, False, False, 0, 0.0, 0.0, 0.0)

                    min5.append([coin, name, symbol, tap, tpp, ms_trend, c_buy, c_sell, wave_count_up, wave_count_down, wave_count_up_after_d, wave_count_down_after_d, 
                                upper, lower, a_up, a_down, b_up, b_down, c_up, c_down, d_up, d_down, ms_buy, ms_sell, laststate, last_a_price_after_d,
                                downprice, upprice, data.iloc[-1]['Close']])
                else:
                    min5.append([coin, name, symbol, tap, tpp, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, False, False, 0, 0.0, 0.0, 0.0, 0.0])

            except Exception as e:
                print(e)
                continue
            
            # 15 minute part
            try:
                timestamp = str(datetime.utcnow().isoformat())[0:19]
                params = urlencode({'AccessKeyId': p_api_key,
                                'SignatureMethod': 'HmacSHA256',
                                'SignatureVersion': '2',
                                'Timestamp': timestamp,
                                'symbol': symbol,
                                'period': '15min',
                                'size': 200
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
                    laststate, last_a_price_after_d, downprice, upprice = market_structure(True, symbol, data, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                                                    0, 0, False, False, 0, 0.0, 0.0, 0.0)

                    min15.append([coin, name, symbol, tap, tpp, ms_trend, c_buy, c_sell, wave_count_up, wave_count_down, wave_count_up_after_d, wave_count_down_after_d, 
                                upper, lower, a_up, a_down, b_up, b_down, c_up, c_down, d_up, d_down, ms_buy, ms_sell, laststate, last_a_price_after_d,
                                downprice, upprice, data.iloc[-1]['Close']])
                else:
                    min15.append([coin, name, symbol, tap, tpp, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, False, False, 0, 0.0, 0.0, 0.0, 0.0])

            except Exception as e:
                print(e)
                continue

            # 60 minute part
            try:
                timestamp = str(datetime.utcnow().isoformat())[0:19]
                params = urlencode({'AccessKeyId': p_api_key,
                                'SignatureMethod': 'HmacSHA256',
                                'SignatureVersion': '2',
                                'Timestamp': timestamp,
                                'symbol': symbol,
                                'period': '60min',
                                'size': 200
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
                    laststate, last_a_price_after_d, downprice, upprice = market_structure(True, symbol, data, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                                                    0, 0, False, False, 0, 0.0, 0.0, 0.0)

                    h1.append([coin, name, symbol, tap, tpp, ms_trend, c_buy, c_sell, wave_count_up, wave_count_down, wave_count_up_after_d, wave_count_down_after_d, 
                                upper, lower, a_up, a_down, b_up, b_down, c_up, c_down, d_up, d_down, ms_buy, ms_sell, laststate, last_a_price_after_d,
                                downprice, upprice, data.iloc[-1]['Close']])
                else:
                    h1.append([coin, name, symbol, tap, tpp, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, False, False, 0, 0.0, 0.0, 0.0, 0.0])

            except Exception as e:
                print(e)
                continue

            # 4 hours part
            try:
                timestamp = str(datetime.utcnow().isoformat())[0:19]
                params = urlencode({'AccessKeyId': p_api_key,
                                'SignatureMethod': 'HmacSHA256',
                                'SignatureVersion': '2',
                                'Timestamp': timestamp,
                                'symbol': symbol,
                                'period': '4hour',
                                'size': 200
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
                    laststate, last_a_price_after_d, downprice, upprice = market_structure(True, symbol, data, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                                                    0, 0, False, False, 0, 0.0, 0.0, 0.0)

                    h4.append([coin, name, symbol, tap, tpp, ms_trend, c_buy, c_sell, wave_count_up, wave_count_down, wave_count_up_after_d, wave_count_down_after_d, 
                                upper, lower, a_up, a_down, b_up, b_down, c_up, c_down, d_up, d_down, ms_buy, ms_sell, laststate, last_a_price_after_d,
                                downprice, upprice, data.iloc[-1]['Close']])
                else:
                    h4.append([coin, name, symbol, tap, tpp, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, False, False, 0, 0.0, 0.0, 0.0, 0.0])

            except Exception as e:
                print(e)
                continue

            # 1 day part
            try:
                timestamp = str(datetime.utcnow().isoformat())[0:19]
                params = urlencode({'AccessKeyId': p_api_key,
                                'SignatureMethod': 'HmacSHA256',
                                'SignatureVersion': '2',
                                'Timestamp': timestamp,
                                'symbol': symbol,
                                'period': '1day',
                                'size': 200
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
                    laststate, last_a_price_after_d, downprice, upprice = market_structure(True, symbol, data, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                                                    0, 0, False, False, 0, 0.0, 0.0, 0.0)

                    d1.append([coin, name, symbol, tap, tpp, ms_trend, c_buy, c_sell, wave_count_up, wave_count_down, wave_count_up_after_d, wave_count_down_after_d, 
                                upper, lower, a_up, a_down, b_up, b_down, c_up, c_down, d_up, d_down, ms_buy, ms_sell, laststate, last_a_price_after_d,
                                downprice, upprice, data.iloc[-1]['Close']])
                else:
                    d1.append([coin, name, symbol, tap, tpp, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, False, False, 0, 0.0, 0.0, 0.0, 0.0])

            except Exception as e:
                print(e)
                continue

df = pd.DataFrame(min1, columns=['Coin', 'Name', 'Symbol', 'PCoin', 'PPrice', 'Trend_1M', 'CBuy', 'CSell', 'WaveCountUp', 'WaveCountDown', 'WaveCountUpAfterD', 'WaveCountDownAfterD', 
                                'Upper', 'Lower', 'AUp', 'ADown', 'BUp', 'BDown', 'CUp', 'CDown', 'DUp', 'DDown', 'MSBuy', 'MSSell', 
                                'LastState', 'LastAPriceAfterD', 'DownPrice', 'UpPrice', 'LPrice'])

df.to_csv("./data/1m.csv", index=False)

df = pd.DataFrame(min5, columns=['Coin', 'Name', 'Symbol', 'PCoin', 'PPrice', 'Trend_5M', 'CBuy', 'CSell', 'WaveCountUp', 'WaveCountDown', 'WaveCountUpAfterD', 'WaveCountDownAfterD', 
                                'Upper', 'Lower', 'AUp', 'ADown', 'BUp', 'BDown', 'CUp', 'CDown', 'DUp', 'DDown', 'MSBuy', 'MSSell', 
                                'LastState', 'LastAPriceAfterD', 'DownPrice', 'UpPrice', 'LPrice'])

df.to_csv("./data/5m.csv", index=False)

df = pd.DataFrame(min15, columns=['Coin', 'Name', 'Symbol', 'PCoin', 'PPrice', 'Trend_15M', 'CBuy', 'CSell', 'WaveCountUp', 'WaveCountDown', 'WaveCountUpAfterD', 'WaveCountDownAfterD', 
                                'Upper', 'Lower', 'AUp', 'ADown', 'BUp', 'BDown', 'CUp', 'CDown', 'DUp', 'DDown', 'MSBuy', 'MSSell', 
                                'LastState', 'LastAPriceAfterD', 'DownPrice', 'UpPrice', 'LPrice'])

df.to_csv("./data/15m.csv", index=False)

df = pd.DataFrame(h1, columns=['Coin', 'Name', 'Symbol', 'PCoin', 'PPrice', 'Trend_H1', 'CBuy', 'CSell', 'WaveCountUp', 'WaveCountDown', 'WaveCountUpAfterD', 'WaveCountDownAfterD', 
                                'Upper', 'Lower', 'AUp', 'ADown', 'BUp', 'BDown', 'CUp', 'CDown', 'DUp', 'DDown', 'MSBuy', 'MSSell', 
                                'LastState', 'LastAPriceAfterD', 'DownPrice', 'UpPrice', 'LPrice'])

df.to_csv("./data/1h.csv", index=False)

df = pd.DataFrame(h4, columns=['Coin', 'Name', 'Symbol', 'PCoin', 'PPrice', 'Trend_4H', 'CBuy', 'CSell', 'WaveCountUp', 'WaveCountDown', 'WaveCountUpAfterD', 'WaveCountDownAfterD', 
                                'Upper', 'Lower', 'AUp', 'ADown', 'BUp', 'BDown', 'CUp', 'CDown', 'DUp', 'DDown', 'MSBuy', 'MSSell', 
                                'LastState', 'LastAPriceAfterD', 'DownPrice', 'UpPrice', 'LPrice'])

df.to_csv("./data/4h.csv", index=False)

df = pd.DataFrame(d1, columns=['Coin', 'Name', 'Symbol', 'PCoin', 'PPrice', 'Trend_1D', 'CBuy', 'CSell', 'WaveCountUp', 'WaveCountDown', 'WaveCountUpAfterD', 'WaveCountDownAfterD', 
                                'Upper', 'Lower', 'AUp', 'ADown', 'BUp', 'BDown', 'CUp', 'CDown', 'DUp', 'DDown', 'MSBuy', 'MSSell', 
                                'LastState', 'LastAPriceAfterD', 'DownPrice', 'UpPrice', 'LPrice'])

df.to_csv("./data/1d.csv", index=False)