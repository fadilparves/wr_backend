import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
from dbconn import connect

conn = connect()
r = []
data = requests.get('https://api.coingecko.com/api/v3/coins/list')
for d in data.json():
    r.append([d['id'], d['symbol'], d['name']])

df = pd.DataFrame(r, columns=["ID", "Coin", "Name"])
df.to_sql("coingeko_info", if_exists='replace', con=conn, index=False)