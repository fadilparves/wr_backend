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

min1 = pd.read_csv("./data/min1.csv")
min5 = pd.read_csv("./data/min5.csv")
min15 = pd.read_csv("./data/min15.csv")
h1 = pd.read_csv("./data/h1.csv")
h4 = pd.read_csv("./data/h4.csv")
d1 = pd.read_csv("./data/d1.csv")

data = min1.merge(min5, on="Symbol", how='left')
data = data.merge(min15, on="Symbol", how='left')
data = data.merge(h1, on="Symbol", how='left')
data = data.merge(h4, on="Symbol", how='left')
data = data.merge(d1, on="Symbol", how='left')

data = data[['Symbol', 'Trend_1M', 'Trend_5M', 'Trend_15M', 'Trend_1H', 'Trend_4H', 'Trend_1D']]
data.fillna(2, inplace=True)

shariah_status = pd.read_csv("./data/shariah_status.csv")
data = data.merge(shariah_status, on='Coin', how='left')

data['Shariah Status'].fillna('Grey', inplace=True)

print(data)