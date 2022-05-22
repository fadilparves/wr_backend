import requests
from bs4 import BeautifulSoup
import pandas as pd

def shariah_status():
    URL = "https://sharlife.my/crypto-shariah"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="accordionExample")
    coins = results.find_all("div", class_="border rounded-3")

    row = []
    for coin in coins:
        coin_name = coin.find("strong", class_="ticker")
        shariah_status = coin.find("div", class_="shariah-status")
        row.append([coin_name.text.strip(), shariah_status.text.strip()])

    df = pd.DataFrame(row, columns=["Coin", "Shariah Status"])
    df.to_csv("shariah_status.csv", index=False)
