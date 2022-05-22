from flask import Flask, jsonify
from flask_cors import CORS
from privateconfig import p_api_key, p_secret_key
from datetime import datetime
import requests
import json
import hmac
import hashlib
import base64
from urllib.parse import urlencode
import pandas as pd

app = Flask(__name__)
CORS(app)

base_uri = 'api-aws.huobi.pro'

def generate_sign(method, base_uri, endpoint, params, secret_key):
    '''
    Generate a request signature for a given method, endpoint, params and secret key.
    '''
    pre_signed_text = method + '\n' + base_uri + '\n' + endpoint + '\n' + params
    hash_code = hmac.new(p_secret_key.encode(), pre_signed_text.encode(), hashlib.sha256).digest()
    signature = urlencode({'Signature': base64.b64encode(hash_code).decode()})

    return signature

@app.route("/ms")
def ms():
    min1 = pd.read_csv("./data/1m.csv")
    min5 = pd.read_csv("./data/5m.csv")
    min15 = pd.read_csv("./data/15m.csv")
    h1 = pd.read_csv("./data/1h.csv")
    h4 = pd.read_csv("./data/4h.csv")
    d1 = pd.read_csv("./data/1d.csv")
    mapping = pd.read_csv("./data/mapping.csv")

    data = min1.merge(min5[['Symbol','Trend_5M']], on="Symbol", how='left')
    data = data.merge(min15[['Symbol','Trend_15M']], on="Symbol", how='left')
    data = data.merge(h1[['Symbol','Trend_H1']], on="Symbol", how='left')
    data = data.merge(h4[['Symbol','Trend_4H']], on="Symbol", how='left')
    data = data.merge(d1[['Symbol','Trend_1D']], on="Symbol", how='left')

    data = data[['Symbol', 'Coin', 'Name', 'LPrice', 'Trend_1M', 'Trend_5M', 'Trend_15M', 'Trend_H1', 'Trend_4H', 'Trend_1D']]
    data.fillna(2, inplace=True)

    shariah_status = pd.read_csv("shariah_status.csv")
    data = data.merge(shariah_status, on='Coin', how='left')

    data['Shariah Status'].fillna('Grey', inplace=True)

    data['Trend_1M'].replace(0, 'Buy', inplace=True)
    data['Trend_1M'].replace(1, 'Sell', inplace=True)
    data['Trend_1M'].replace(2, 'Sideway', inplace=True)

    data['Trend_5M'].replace(0, 'Buy', inplace=True)
    data['Trend_5M'].replace(1, 'Sell', inplace=True)
    data['Trend_5M'].replace(2, 'Sideway', inplace=True)

    data['Trend_15M'].replace(0, 'Buy', inplace=True)
    data['Trend_15M'].replace(1, 'Sell', inplace=True)
    data['Trend_15M'].replace(2, 'Sideway', inplace=True)

    data['Trend_H1'].replace(0, 'Buy', inplace=True)
    data['Trend_H1'].replace(1, 'Sell', inplace=True)
    data['Trend_H1'].replace(2, 'Sideway', inplace=True)

    data['Trend_4H'].replace(0, 'Buy', inplace=True)
    data['Trend_4H'].replace(1, 'Sell', inplace=True)
    data['Trend_4H'].replace(2, 'Sideway', inplace=True)

    data['Trend_1D'].replace(0, 'Buy', inplace=True)
    data['Trend_1D'].replace(1, 'Sell', inplace=True)
    data['Trend_1D'].replace(2, 'Sideway', inplace=True)

    r = []

    for _, row in data.iterrows():
        a = []
        class_1min = ""
        class_5min = ""
        class_15min = ""
        class_1h = ""
        class_4h = ""
        class_1d = ""
        class_shariah = ""

        if row['Trend_1M'] == 'Buy':
            class_1min = "color-price-up"
        elif row['Trend_1M'] == 'Sell':
            class_1min = "color-price-down"
        else:
            class_1min = ""

        if row['Trend_5M'] == 'Buy':
            class_5min = "color-price-up"
        elif row['Trend_5M'] == 'Sell':
            class_5min = "color-price-down"
        else:
            class_5min = ""

        if row['Trend_15M'] == 'Buy':
            class_15min = "color-price-up"
        elif row['Trend_15M'] == 'Sell':
            class_15min = "color-price-down"
        else:
            class_15min = ""

        if row['Trend_H1'] == 'Buy':
            class_1h = "color-price-up"
        elif row['Trend_H1'] == 'Sell':
            class_1h = "color-price-down"
        else:
            class_1h = ""

        if row['Trend_4H'] == 'Buy':
            class_4h = "color-price-up"
        elif row['Trend_4H'] == 'Sell':
            class_4h = "color-price-down"
        else:
            class_4h = ""

        if row['Trend_1D'] == 'Buy':
            class_1d = "color-price-up"
        elif row['Trend_1D'] == 'Sell':
            class_1d = "color-price-down"
        else:
            class_1d = ""

        if row['Shariah Status'] == 'Shariah':
            class_shariah = "color-price-up"
        elif row['Shariah Status'] == 'Non-Shariah':
            class_shariah = "color-price-down"
        else:
            class_shariah = ""

        temp = mapping[mapping['Coin'] == row['Coin']]

        if len(temp) > 0:
            img_src = "https://s2.coinmarketcap.com/static/img/coins/64x64/{}.png".format(temp.iloc[0]['ID'])
        else:
            temp = mapping[mapping['Coin'].str.contains(row['Coin'])]
            if len(temp) > 0:
                img_src = "https://s2.coinmarketcap.com/static/img/coins/64x64/{}.png".format(temp.iloc[0]['ID'])
            else:
                img_src = "assets/images/coin/BTC.png"

        a.append("""<tr><td><img src="{}" alt="" class="img-fluid avatar mx-1"><span class="text-uppercase fw-bold"> {} </span> <span class="text-muted"> {}</span></td>""".format(img_src, row['Name'], row['Coin']))
        a.append("""<td><span class="">{}</span></td>""".format(row['LPrice']))
        a.append("""<td><span class="{}">{}</span></td>""".format(class_1min, row['Trend_1M']))
        a.append("""<td><span class="{}">{}</span></td>""".format(class_5min, row['Trend_5M']))
        a.append("""<td><span class="{}">{}</span></td>""".format(class_15min, row['Trend_15M']))
        a.append("""<td><span class="{}">{}</span></td>""".format(class_1h, row['Trend_H1']))
        a.append("""<td><span class="{}">{}</span></td>""".format(class_4h, row['Trend_4H']))
        a.append("""<td><span class="{}">{}</span></td>""".format(class_1d, row['Trend_1D']))
        a.append("""<td><span class="{}">{}</span></td>""".format(class_shariah, row['Shariah Status']))

        r.append(a)

    return jsonify(r)

@app.route('/basic')
def basic():
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
        class_span = ""
        class_price = ""

        if data.iloc[-1]['Close'] > data.iloc[0]['Close']:
            difference = "+" + str(round(difference, 2)) + "%"
            class_fa = "fa fa-level-up"
            class_span = "small text-success"
            class_price = "fs-6 fw-bold color-price-up"
        elif data.iloc[-1]['Close'] < data.iloc[0]['Close']:
            difference = str(round(difference, 2)) + "%"
            class_fa = "fa fa-level-down"
            class_span = "small text-danger"
            class_price = "fs-6 fw-bold color-price-down"
        else:
            difference = "0.00%"
            class_fa = ""
            class_span = "small text-muted"
            class_price = "fs-6 fw-bold"
        
        difference = """<span class="{}">{} <i class="{}"></i></span>""".format(class_span, difference, class_fa)
        price = """<span class="{}">{}</span>""".format(class_price, data.iloc[-1]['Close'])
        rums.append([symbol, difference, price])
    
    return jsonify(rums)