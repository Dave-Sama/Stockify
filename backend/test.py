import yfinance as yf
import time

def fetch_stock_data(ticker, period="1mo", retries=3):
    stock = yf.Ticker(ticker)
    for attempt in range(retries):
        try:
            data = stock.history(period=period)
            if data.empty:
                print(f"No data found for {ticker} on attempt {attempt + 1}")
                if attempt == retries - 1:
                    return None
                time.sleep(2)  # Wait before retrying
                continue
            print(f"Successfully fetched data for {ticker}: {len(data)} rows")
            return data
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == retries - 1:
                print(f"Failed to fetch {ticker} after {retries} attempts")
                return None
            time.sleep(2)  # Wait before retrying

# Test it
data = fetch_stock_data("NVDA", period="3mo")
if data is not None:
    print(data)
else:
    print("No data retrieved")

print("hello")