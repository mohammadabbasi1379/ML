import yfinance as yf
from GoogleNews import GoogleNews
import pandas as pd
import numpy as np
from datetime import datetime

symbols = {
    'GC=F': 'Gold Futures',
    'CL=F': 'Crude Oil Futures',
    'DX-Y.NYB': 'US Dollar Index'
}

def fetch_financial_data(stock_symbol, start_date, end_date):
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    return stock_data

def get_news(query, start_date, end_date):
    googlenews = GoogleNews()
    googlenews.set_time_range(start_date, end_date)
    googlenews.search(query)
    news_result = googlenews.results()
    return news_result

def get_data_and_news(symbol, start_date, end_date, news_query):
    stock_data = fetch_financial_data(symbol, start_date, end_date)
    news = get_news(news_query, start_date, end_date)

    stock_data['Symbol'] = symbols[symbol]
    stock_data.reset_index(inplace=True)
    stock_data.rename(columns={'Date': 'Time'}, inplace=True)

    stock_data = stock_data[['Symbol', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']]

    news_text = ""
    for item in news:
        news_text += item['title'] + ". "

    news_data = {'Symbol': [symbols[symbol]], 'Time': [start_date], 'News': [news_text]}
    df_news = pd.DataFrame(news_data)

    return stock_data, df_news

end_date = datetime.now().strftime('%Y-%m-%d')

gold_data, gold_news = get_data_and_news('GC=F', '2021-01-01', end_date, 'gold')
oil_data, oil_news = get_data_and_news('CL=F', '2021-01-01', end_date, 'crude oil')
dollar_data, dollar_news = get_data_and_news('DX-Y.NYB', '2021-01-01', end_date, 'dollar index')

for data in [gold_data, oil_data, dollar_data]:
    data.replace(0, np.NaN, inplace=True)

result = pd.concat([gold_data, oil_data, dollar_data])
result_news = pd.concat([gold_news, oil_news, dollar_news])

merged_data = pd.concat([result.set_index(['Time', 'Symbol']), result_news.set_index(['Time', 'Symbol'])], axis=1, join='outer').reset_index()

print(merged_data)
