import pandas_datareader as pdr
import mplfinance as mplf
import datetime

crypto = 'BTC'
currency = 'EUR'

#From 1st January 2020 until now
start = datetime.datetime(2020,1,1)
end = datetime.datetime.now()

#Plot value of Bitcoin over years
data = pdr.DataReader(f'{crypto}-{currency}', 'yahoo', start, end)
mplf.plot(data, type='candle', volume=True, style='yahoo')