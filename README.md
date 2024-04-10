This is a project to help with technical analysis of stocks after the market
closes to provide daily information about price activity on set range of
stocks. The project uses Pandas and Yahoo Finance to leverage these
calculations.

get_price is a function that is called daily to fetch daily closing values of
stocks

calculate_technicals is run after the prices are fetched to calculate most up
to date: 50 moving average, 200 day moving average and dividend rate. This can
be used as a tool to find interesting stocks to take a closer look at

plot_stock is used to see graphical presentation of the the stocks performance
over days to years
