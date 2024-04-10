#!/usr/bin/python
import pandas as pd
import yfinance as yf
import datetime
import csv
import list_of_stocks
import time

from csv import writer
from sys import argv

ticker = argv[1]

# stock = 'CREE'


print(ticker)
time.sleep(5)
ticker_yahoo = yf.Ticker(ticker)

data = ticker_yahoo.history(period='1024mo')

print(data['Close'])

# This will rename the Close to Closing Price which is what Cree Closer uses
data['Closing Price'] = data['Close']

with open(ticker + '.csv', mode = 'r+') as f:
    csv_reader = writer(f)
    data['Closing Price'].to_csv(f)
    #csv_reader.writerows(map(lambda x: [x], data['Close']))

