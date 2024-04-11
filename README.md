This is a project to help with technical analysis of stocks after the market
closes to provide daily information about price activity on set range of
stocks. The project uses Pandas and Yahoo Finance to leverage these
calculations.

get_price.py is a collection of functions that are called daily to fetch daily
closing values of stocks after the market close happens. It is recommended to
run this script daily using crontab or similar automatic scheduler.

get_historical_closing_price.py is a collection of functions that can be called
to fetch historical trading prices all at once for a single stock. This script
is intended to be ran one off when needed.

calculate_technicals.py is run after the prices are fetched to calculate most up
to date: 50 moving average, 200 day moving average and dividend rate. This can
be used as a tool to find interesting stocks to take a closer look at

plot_stock.py is used to see graphical presentation of the the stocks
performance over days to years. This will show 50-day and 200-day moving
averages as well to determine technical opportunities to trade.

