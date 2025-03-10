from app import create_app
import argparse
import subprocess
import sys
import os
import socket

def run_cli():
    parser = argparse.ArgumentParser(description="Stock Data CLI")
    subparsers = parser.add_subparsers(dest="command")
    fetch = subparsers.add_parser("fetch", help="Fetch and save stock data")
    fetch.add_argument("ticker", help="Stock ticker symbol")
    fetch.add_argument("--period", default="100d", help="Time period (e.g., 100d)")
    fetch.add_argument("--start", help="Start date (YYYY-MM-DD)")
    fetch.add_argument("--end", help="End date (YYYY-MM-DD)")
    fetch.add_argument("--path", help="Output directory")
    fetch.add_argument("--format", choices=["csv", "json"], default="csv")
    args = parser.parse_args()
    if args.command == "fetch":
        from app.data import load_data, save_data
        if args.period and (args.start or args.end):
            print("Error: Use either --period or --start/--end, not both")
            return
        if not args.period and (not args.start or not args.end):
            print("Error: --start and --end required together")
            return
        data = load_data(args.ticker, args.period, args.start, args.end)
        save_data(data, args.ticker, args.path, args.format)
    else:
        parser.print_help()

def is_port_in_use(host: str = "localhost", port: int = 3000) -> bool:
    """
    Check if a port is in use on the given host.
    Returns True if the port is occupied, False if free.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return False
        except OSError:
            return True

if __name__ == "__main__":
    if len(sys.argv) > 1:  # CLI mode
        run_cli()
    else:  # API mode
        # Start the frontend if port 3000 is free
        frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))
        frontend_launched = False
        if os.path.exists(frontend_dir):
            print(f"Checking frontend directory: {frontend_dir}")
            if not is_port_in_use("localhost", 3000):
                try:
                    # Launch frontend in the background without capturing output
                    cmd = f'cd /d "{frontend_dir}" && npm start'
                    subprocess.Popen(cmd, shell=True)
                    print("Starting frontend at http://localhost:3000... (running in background)")
                    frontend_launched = True
                except Exception as e:
                    print(f"Failed to start frontend: {e}")
            else:
                print("Port 3000 is already in use. Skipping frontend launch.")
        else:
            print("Frontend directory not found. Skipping frontend launch.")

        # Start the Flask backend (runs independently)
        app = create_app()
        app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=not frontend_launched)