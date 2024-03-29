
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
from privateconfig import coinmarketcap_key
from dbconn import connect

def crypto_info():
    conn = connect()
    rng = [1, 5001, 10001, 15001, 20001, 25001, 30001, 35001, 40001, 45001, 55001, 60001, 65001, 70001, 75001, 80001, 85001, 90001, 95001, 100000]

    rum = []
    for r in rng:
        start = r
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
        parameters = {
        'start': start,
        }

        headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': coinmarketcap_key,
        }

        session = Session()
        session.headers.update(headers)

        try:
            row = []
            response = session.get(url, params=parameters)
            data = json.loads(response.text)

            if 'data' in data:
                print(start)
                for d in data['data']:
                    row.append([d['id'], d['symbol'], "https://s2.coinmarketcap.com/static/img/coins/64x64/{}.png".format(d['id'])])
            else:
                break

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

        df = pd.DataFrame(row, columns=["ID", "Coin", "Icon"])
        rum.append(df)
        
    df = pd.concat(rum, axis=0)
    df.drop_duplicates(subset=['ID', 'Coin', 'Icon'], keep='first', inplace=True)
    # df.to_csv("./data/mapping.csv", index=False)
    df.to_sql("mapping_coins", if_exists='replace', con=conn, index=False)
