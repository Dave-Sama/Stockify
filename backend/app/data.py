# Houses load_data() and save_data() for stock data logic.

import yfinance as yf
from pathlib import Path
import time

DEFAULT_PERIOD = "100d"
DEFAULT_FORMAT = "csv"

def load_data(ticker: str, period: str = DEFAULT_PERIOD, start: str = None, end: str = None, retries: int = 3) -> "pd.DataFrame":
    stock = yf.Ticker(ticker)
    print("@@@@@@@@@@@@@@@@@" , start, end)
    for attempt in range(retries):
        try:
            if start and end:
                data = stock.history(start=start, end=end)
            else:
                data = stock.history(period=period)
            if data.empty:
                raise ValueError(f"No data found for {ticker}")

            # Data Cleansing
            # Select relevant columns
            relevant_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            # Ensure only the specified columns are kept
            data = data[relevant_columns]

            # Remove duplicates (based on date index)
            data = data[~data.index.duplicated(keep='first')]

            # Handle missing values
            # Drop rows where all values are NaN
            data = data.dropna(how='all')
            # Forward-fill remaining NaNs (e.g., missing prices due to holidays)
            data = data.fillna(method='ffill')

            if data.empty:
                raise ValueError(f"No valid data after cleaning for {ticker}")

            print(f"Successfully fetched and cleaned data for {ticker}: {len(data)} rows")
            return data

        except Exception as e:
            if attempt < retries - 1:
                print(f"Attempt {attempt + 1} failed for {ticker}: {e}. Retrying in 2s...")
                time.sleep(2)
            else:
                raise ValueError(f"Failed to fetch data for {ticker} after {retries} attempts: {e}")
def analyze_data(ticker: str, data: "pd.DataFrame") -> dict:
    """
    Analyze stock data characteristics using pandas.
    Returns a dictionary with summary statistics and metadata.
    """
    analysis = {
        "ticker": ticker,
        "row_count": len(data),
        "columns": list(data.columns),
        # Convert dtypes to strings for JSON serialization
        "data_types": {col: str(dtype) for col, dtype in data.dtypes.items()},
        "missing_values": data.isna().sum().to_dict(),
        "basic_stats": data.describe().to_dict(),
        "date_range": {
            "start": data.index[0].strftime("%Y-%m-%d"),
            "end": data.index[-1].strftime("%Y-%m-%d")
        }
    }
    return analysis

def save_data(data: "pd.DataFrame", ticker: str, path: str = None, format: str = DEFAULT_FORMAT) -> None:
    format = format.lower() if format else DEFAULT_FORMAT
    # If path is provided, use it; otherwise, use downloads next to this file
    if path:
        prefix = Path(path) / "downloads"
    else:
        # Get the directory of the current file (data.py), then go up and into downloads
        prefix = Path(__file__).parent / "downloads"
    filename = prefix / f"{ticker}_data.{format}"
    try:
        # Ensure the downloads directory exists
        prefix.mkdir(parents=True, exist_ok=True)
        if format == "csv":
            data.to_csv(filename)
        elif format == "json":
            data.to_json(filename)
        else:
            raise ValueError(f"Unsupported format: {format}")
        print(f"Data saved to '{filename}'")
    except Exception as e:
        print(f"Error saving data: {e}")
