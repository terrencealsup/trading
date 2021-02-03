import requests
import numpy as np
import pandas as pd
from datetime import datetime

# yahoo finance identifies securities by ticker, which is availabe in crsp.dsfhdr
def get_price_history_yahoo_finance(ticker, frequency='1d', begin_time=1546322400, finish_time=int(datetime.now().timestamp())):
    """
        read price data from yahoo finance
        args:
            ticker
            frequency: '1d' or '1wk' or '1mo'
            begin_time: int, epoch time, default is 1/1/2019
            finish_time: int, epoch time, default is current time
    """
    # define endpoint for making web request
    endpoint = fr"https://query1.finance.yahoo.com/v7/finance/download/{ticker}"
    param_dict = {
        'period1': begin_time,
        'period2': finish_time,
        'interval': frequency,
        'events': 'history',
        'includeAdjustedClose': 'true'
    }
    response = requests.get(url=endpoint, params=param_dict)
    if response.status_code == 200:
        df = pd.read_csv(response.url)
    else:
        raise Exception(f"broken url for {ticker}")

    df = df[['Date', 'Adj Close', 'Volume']].astype({'Date': np.datetime64}).set_index('Date')
    return df


df = pd.read_csv('constituents.csv')
tickers = df['Symbol'].astype(str).tolist()


DATA = {}
for i, t in enumerate(tickers):
    DATA[t] = get_price_history_yahoo_finance(t)
    print("{:0.1f}%".format(100 * i/505))

# adding the key in
for key in DATA.keys():
    DATA[key]['Ticker'] = key

# concatenating the DataFrames
DATA = pd.concat(DATA.values())
DATA.to_csv('raw_data.csv')
