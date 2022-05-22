
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
parameters = {
  'start':'1',
  'limit':'5000',
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '65cd29ec-9372-4188-8cd4-7e1583b5c336',
}

session = Session()
session.headers.update(headers)

try:
    row = []
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    for d in data['data']:
        row.append([d['id'], d['symbol']])
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

df = pd.DataFrame(row, columns=["ID", "Coin"])
df.to_csv("mapping.csv", index=False)