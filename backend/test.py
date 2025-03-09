import yfinance as yf
stock = yf.Ticker("AAPL")
data = stock.history(period="1mo")
print(data)