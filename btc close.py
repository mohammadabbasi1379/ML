import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

coins_symbols = [
    "BTC", "ETH", "USDT", "BNB", "ADA", "XRP", "SOL", "DOT", "DOGE", "USDC",
    "TRX", "TWT", "BTT", "SHIB", "LTC", "LINK", "BCH", "XLM", "ALGO", "XTZ",
    "EOS", "UNI", "XMR", "AXS", "VET", "FIL", "AAVE", "TRONPAD", "CAKE", "KSM",
    "ZIL", "TRXBLACK", "BSV", "TRXC", "TRXH", "TRXSCAN", "TRXV", "TRXEX", "TRXW",
    "TRXX"
]

data = {}
for symbol in coins_symbols:
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="100d")
    if not hist.empty:
        close_prices = hist["Close"]
        data[symbol] = close_prices

df = pd.DataFrame(data)

df = df.T

df = df.fillna(df.mean(axis=0))

kmeans = KMeans(n_clusters=3, random_state=0)
kmeans.fit(df)
labels = kmeans.labels_

df["Cluster"] = labels

print(df)
