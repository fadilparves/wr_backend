from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route("/ms")
def ms():
    min1 = pd.read_csv("./data/1m.csv")
    min5 = pd.read_csv("./data/5m.csv")
    min15 = pd.read_csv("./data/15m.csv")
    h1 = pd.read_csv("./data/1h.csv")
    h4 = pd.read_csv("./data/4h.csv")
    d1 = pd.read_csv("./data/1d.csv")

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

        a.append("""<tr><td><img src="assets/images/coin/BTC.png" alt="" class="img-fluid avatar mx-1"><span class="text-uppercase fw-bold"> {} </span> <span class="text-muted"> {}</span></td>""".format(row['Name'], row['Coin']))
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

