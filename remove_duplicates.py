import csv
import list_of_stocks

tickers = list_of_stocks.tickers
found_issue = False

for ticker in tickers:
    seen = []
    with open((ticker + '.csv'), mode = 'r+') as f:
        for line in f:
            line_lower = line.lower()[:10]
            if line_lower in seen:
                print(f)
                print(line)
                found_issue = True
            else:
                seen.append(line_lower)

if not found_issue:
    print("Everything is awesome, no issues found")
