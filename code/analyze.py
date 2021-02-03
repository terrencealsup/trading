import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

DATA = pd.read_csv('raw_data.csv', parse_dates = ['Date'], index_col = ['Date', 'Ticker'])

tickers = DATA.index.unique(level = 'Ticker').values.tolist()
dates = DATA.index.unique(level = 'Date').values.tolist()[1:]


RET = pd.DataFrame(index = DATA.index.unique(level = 'Date')[1:])

for t in tickers:
    xst = DATA.xs(t, level = 'Ticker')
    RET[t] = xst['Adj Close'].pct_change().dropna()


start = datetime(2020, 12, 1)
end = datetime(2021, 2, 1)

lookback = RET.loc[start:end]

print(lookback)

ret6mo = (1 + lookback).prod() - 1
ret6mo.sort_values(ascending = False, inplace = True)
print(ret6mo.head(10))
