# import requests
# from bs4 import BeautifulSoup
import pandas as pd

# URL = "https://sharlife.my/crypto-shariah"
# page = requests.get(URL)

# soup = BeautifulSoup(page.content, "html.parser")
# results = soup.find(id="accordionExample")
# coins = results.find_all("div", class_="border rounded-3")

# row = []
# for coin in coins:
#     coin_name = coin.find("strong", class_="ticker")
#     shariah_status = coin.find("div", class_="shariah-status")
#     row.append([coin_name.text.strip(), shariah_status.text.strip()])

# df = pd.DataFrame(row, columns=["Coin", "Shariah Status"])
# df.to_csv("shariah_status.csv", index=False)

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

data = data[['Symbol', 'Coin', 'Name', 'Trend_1M', 'Trend_5M', 'Trend_15M', 'Trend_H1', 'Trend_4H', 'Trend_1D']]
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
        class_1d = "color-price-up"
    elif row['Shariah Status'] == 'Non-Shariah':
        class_1d = "color-price-down"
    else:
        class_1d = ""
        
    a = """ <tr><td><img src="assets/images/coin/BTC.png" alt="" class="img-fluid avatar mx-1"><span class="text-uppercase fw-bold"> {} </span> <span class="text-muted"> {}</span></td>
        <td><span class="">{}</span></td>
        <td><span class="{}">{}</span></td>
        <td><span class="{}">{}</span></td>
        <td><span class="{}">{}</span></td>
        <td><span class="{}">{}</span></td>
        <td><span class="{}">{}</span></td>
        <td><span class="{}">{}</span></td>
        <td><span class="{}">{}</span></td></tr> """.format(row['Name'], row['Coin'], row['LPrice'],
                                                            class_1min, row['Trend_1M'], 
                                                            class_5min, row['Trend_5M'], 
                                                            class_15min, row['Trend_15M'], 
                                                            class_1h, row['Trend_H1'], 
                                                            class_4h, row['Trend_4H'], 
                                                            class_1d, row['Trend_1D'],
                                                            row['Shariah Status'])

    r.append(a)

print(data)
print(r)