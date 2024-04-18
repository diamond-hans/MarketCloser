import pandas as pd
import csv
import list_of_stocks
import numpy as np
import math
from heapq import nlargest
from operator import itemgetter

tickers = list_of_stocks.tickers

stocks_under_RSI_30 = []

stocks_over_RSI_70 = []

stocks_under_50_day = []

stocks_under_200_day = []

stocks_over_50_day = []

stocks_over_200_day = []

stocks_new_high = []

stocks_new_low = []

top_dividends = []

dividend_changed = []

dividend_diff = []

dividend = 0

dividend_percentage = 0

print("Ticker, \tClosing Price, \tChange %, \tRSI. \t\t50-Day MA, \t\t"+
        "200-Day Ma, \tDividend \tDividend %")

for ticker in tickers:
    file_to_read = ticker + '.csv'
    df = pd.read_csv(file_to_read)

    #print(df)

    # find highest value
    highest_close = df['Closing Price'].max()
    lowest_close = df['Closing Price'].min()
    
    #if len(df['Dividend Rate']) == 0 or math.isnan(df['Dividend Rate'].iloc[-1]) == True:
    #    dividend = 0
    #else:
    #    dividend = df['Dividend Rate'].iloc[-1]

    dividend_percentage = dividend / df['Closing Price'].iloc[-1] * 100
    
    top_dividends.append((str(ticker),dividend_percentage))

    #print(highest_close)

    #calculate change
    change = df['Closing Price'].diff()

    df['Change'] = change

    #calculate dividend change commented out due to issues with yahoofinance
    '''
    if math.isnan(df['Dividend Rate'].iloc[-1]):
        div_change = 0
    else:
        div_change = df['Dividend Rate'].diff()
    
    df['Dividend Change'] = div_change

    # Has dividend changed?
    if  df['Dividend Change'].iloc[-1] != 0:
        dividend_changed.append(ticker)
        dividend_diff.append(df['Dividend Change'].iloc[-1])

    #print(change)
    '''
    #calculate percentage change
    percentage_change = (df['Closing Price'].pct_change() * 100)

    df['%'] = percentage_change

    #print(percentage_change)

    #see if change is positive or negative

    gain = change.clip(lower = 0)

    loss = -1 * change.clip(upper = 0)

    avg_gain = gain.ewm(com = 14, adjust = False).mean()

    avg_loss = loss.ewm(com = 14, adjust = False).mean()

    relative_strength = avg_gain / avg_loss

    df['Gain'] = gain

    df['Loss'] = loss

    df['Avg Gain'] = avg_gain

    df['Avg Loss'] = avg_loss

    df['Relative Strength'] = relative_strength

    
    if len(df['Closing Price']) >= 14:
        df['RSI'] = 100 - (100/(1+relative_strength))
        threshold = 14
        #df['RSI'].iloc[len(df['RSI'])] = np.nan
        df['RSI'] = df['RSI'].iloc[threshold:]
    else:
        df['RSI'] = np.nan

    if df['RSI'].iloc[-1] <= 30:
        stocks_under_RSI_30.append(ticker)

    if df['RSI'].iloc[-1] >= 70:
        stocks_over_RSI_70.append(ticker)
    
    # Determine New All Time High
    if df['Closing Price'].iloc[-1] == highest_close:
       stocks_new_high.append(ticker)

    if df['Closing Price'].iloc[-1] == lowest_close:
       stocks_new_low.append(ticker)


    df['50-Day Moving Average'] = np.round(df.iloc[:,1].rolling(window=50)\
            .mean(),2)
    
    df['200-Day Moving Average'] = np.round(df.iloc[:,1].rolling(window=200)\
            .mean(),2)
    # See if stock is under 50 day moving average
    if df['50-Day Moving Average'].iloc[-1] >= df['Closing Price'].iloc[-1]:
        stocks_under_50_day.append(ticker)
    # See if stock is over 50 day moving average
    if df['50-Day Moving Average'].iloc[-1] < df['Closing Price'].iloc[-1]:
        stocks_over_50_day.append(ticker)
    # See if stock is under 200 day moving average
    if df['200-Day Moving Average'].iloc[-1] >= df['Closing Price'].iloc[-1]:
        stocks_under_200_day.append(ticker)
    # See if stock is over 200 day moving average
    if df['200-Day Moving Average'].iloc[-1] < df['Closing Price'].iloc[-1]:
        stocks_over_200_day.append(ticker)


    # Find common 200 and 50 day stocks (above and below)
    stocks_below_averages = set(stocks_under_50_day).intersection(stocks_under_200_day)
    stocks_above_averages = set(stocks_over_50_day).intersection(stocks_over_200_day)

    save_data = df.to_csv(ticker + 'Pandas.csv', index = True)
    """
    print(ticker, "\t\t", "%.2f"% df['Closing Price'].iloc[-1],"\t\t",\
            "%.2f" % df['%'].iloc[-1],"%",\
            "%.2f" % df['RSI'].iloc[-1])
    """
    print('{}\t\t {:.2f}, \t {:.2f} %, \t {:.2f}, \t {}, \t\t {}, \t{:.2f},'
            '\t\t{:.2f}'.format(\
            ticker,df['Closing Price'].iloc[-1],df['%'].iloc[-1],\
            df['RSI'].iloc[-1], df['50-Day Moving Average'].iloc[-1],\
            df['200-Day Moving Average'].iloc[-1], dividend,\
            dividend_percentage))

# Results
print("Stocks under 50 day moving average: {}".format(stocks_under_50_day))
print("Stocks under 200 day moving average: {}".format(stocks_under_200_day))
print("Stocks under both moving averages: {}".format(stocks_below_averages))
print("Stocks over both moving averages: {}".format(stocks_above_averages))
print("Oversold stocks: {}".format(stocks_under_RSI_30))
print("Overbought stocks: {}".format(stocks_over_RSI_70))
print("Stocks new All Time High: {}".format(stocks_new_high))
print("Stocks new All Time Low: {}".format(stocks_new_low))
# Calculation for top 10 dividends
top_10_dividends = nlargest(10,top_dividends,key=itemgetter(1))
print("Top 10 Dividends:")
for x in top_10_dividends:
    div_percentage ="{:.2f}".format(x[1])
    print(x[0], div_percentage, "%")
if dividend_changed:
    for i in range(len(dividend_changed)):
        print("Dividend changed: {}".format(dividend_changed[i]))
        print("Changed {:.4f}".format(dividend_diff[i]))
