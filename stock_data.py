from datetime import datetime as dt
import pandas as pd
from tvDatafeed import TvDatafeed, Interval

# Connection TradingView
username = 'fgiacobe'
password = open('accessdata.txt', 'r').read()

tv = TvDatafeed(username, password)

tv.search_symbol('PETR4')

def filtered_ticker(ticker=str, start=str, end=str):
    ativo = tv.get_hist(
        symbol=ticker,
        exchange='BMFBOVESPA',
        interval=Interval.in_5_minute,
        n_bars=10000,
        fut_contract=None,
        extended_session=False,
    )
    ativo['symbol'] = ativo['symbol'].apply(lambda x: x.split(':')[1])
    start_day = dt.strptime(start, '%d-%m-%Y').date()
    end_day = dt.strptime(end, '%d-%m-%Y').date()
    ativo_filtered = ativo[(ativo.index.date >= start_day) & (ativo.index.date <= end_day)]
    return ativo_filtered

ticker = filtered_ticker(ticker='PETR4', start='25-01-2023', end='26-01-2023')

ticker['mma5'] = ticker.rolling(window=5)['close'].mean()
ticker['mma5'].plot()
ticker['close'].plot()