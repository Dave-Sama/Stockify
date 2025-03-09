from app import create_app
import argparse
from app.data import load_data, save_data

def run_cli():
    parser = argparse.ArgumentParser(description="Stock Data CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    fetch = subparsers.add_parser("fetch", help="Fetch and save stock data")
    fetch.add_argument("ticker", help="Stock ticker symbol (e.g., NVDA)")
    fetch.add_argument("--period", default="100d", help="Time period (e.g., 100d, 1y)")
    fetch.add_argument("--start", help="Start date (YYYY-MM-DD)")
    fetch.add_argument("--end", help="End date (YYYY-MM-DD)")
    fetch.add_argument("--path", help="Output directory path")
    fetch.add_argument("--format", choices=["csv", "json"], default="csv", help="Output format (csv or json)")
    args = parser.parse_args()
    if args.command == "fetch":
        data = load_data(args.ticker, args.period, args.start, args.end)
        save_data(data, args.ticker, args.path, args.format)
    else:
        parser.print_help()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:  # CLI mode
        run_cli()
    else:  # API mode
        app = create_app()
        app.run(debug=True, host="0.0.0.0", port=5000)