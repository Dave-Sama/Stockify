from flask import Blueprint, request, jsonify
from .data import load_data, analyze_data
from .plotting import generate_plot  # Correct function name

# Define the Blueprint for API routes
api = Blueprint('api', __name__)

@api.route('/plot', methods=['POST'])
def plot_stock():
    """
    Generate a stock plot based on ticker, period or start/end dates, and plot type.
    Expects JSON payload: { "ticker": str, "period": str | "start": str, "end": str, "plot_type": str }
    Returns JSON with Plotly plot data or an error message.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    ticker = data.get('ticker')
    period = data.get('period')
    start = data.get('start')
    end = data.get('end')
    plot_type = data.get('plot_type', 'close')
    

    if not ticker:
        return jsonify({'error': 'Ticker is required'}), 400

    if period and (start or end):
        return jsonify({'error': 'Provide either period or start/end dates, not both'}), 400
    if not period and (not start or not end):
        return jsonify({'error': 'Start and end dates are required when not using period'}), 400

    try:
        if period:
            stock_data = load_data(ticker, period=period)
            
        else:
            stock_data = load_data(ticker, start=start, end=end)

        if stock_data is None or stock_data.empty:
            return jsonify({'error': f'No data found for {ticker}'}), 404
        
        # Call generate_plot with correct argument order: ticker, data, plot_type
        
        plot = generate_plot(ticker, stock_data, plot_type)
        return jsonify({'plot': plot})

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@api.route('/analyze/<ticker>', methods=['GET'])
def analyze_stock(ticker):
    """
    Analyze stock data characteristics for the given ticker.
    Query params: period (default: 100d), start, end.
    Returns JSON with data summary.
    """
    period = request.args.get('period', '100d')
    start = request.args.get('start')
    end = request.args.get('end')

    if period and (start or end):
        return jsonify({'error': 'Provide either period or start/end dates, not both'}), 400
    if not period and (not start or not end):
        return jsonify({'error': 'Start and end dates are required when not using period'}), 400

    try:
        if period:
            stock_data = load_data(ticker, period=period)
        else:
            stock_data = load_data(ticker, start=start, end=end)

        if stock_data is None or stock_data.empty:
            return jsonify({'error': f'No data found for {ticker}'}), 404

        analysis = analyze_data(ticker, stock_data)
        return jsonify(analysis)

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500