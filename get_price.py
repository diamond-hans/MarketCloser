#!/usr/bin/python

import yfinance as yf
import datetime
import csv
from csv import writer
# Internal files to import
import markets_close 
import list_of_stocks

today = datetime.datetime.now().strftime("%Y-%m-%d")

# First check if today is a holiday
# Holidays are stored in a config file called markets_close.py
for i in markets_close.days_closed:
    if i == today:
        raise Exception("Today " + str(today) + " markets are closed")

# Load current tickers from a config file called list_of_stocks.py
tickers = list_of_stocks.tickers

def append_list_as_row(file_name, list_of_elements):
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elements)
        #print("Added " + str(today) + str(ticker) + str(last_quote))

for ticker in tickers:
    with open((ticker + '.csv'), mode = 'r+') as f:
        csv_reader = csv.reader(f)
        value_was_found = False
        for row in csv_reader:
            for values in row:
                if values == today:
                    print("Value for today already submitted")
                    value_was_found = True
    if value_was_found == False:
        count = 1
        #while count <= 3:
        try:
            ticker_yahoo = yf.Ticker(ticker)
            data = ticker_yahoo.history()
            last_quote = (data.tail(1)['Close'].iloc[0])

        except:
        #    count = count + 1
            print("Couldn't get all data")
            data.tail(1)['Close'].iloc[0] = "Bad"
        #if count == 1:
        #    last_quote = (data.tail(1)['Close'].iloc[0])
            #dividend = ticker_yahoo.info['dividendRate']
            #print(today, ticker,last_quote, dividend)

    with open((ticker + '.csv'), mode = 'r+') as f:
        csv_reader = csv.reader(f)
        value_was_found = False
        for row in csv_reader:
            for values in row:
                # This is for debugging purposes and prints all rows in all files
                #print(values)
                if values == today:
                    print("Value for today already submitted")
                    value_was_found = True
    if value_was_found == False and count == 1:
        row_contents = [today, last_quote]
        append_list_as_row((ticker+'.csv'), row_contents)
