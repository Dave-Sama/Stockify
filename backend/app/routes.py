from flask import Blueprint, request, jsonify
from .data import load_data, analyze_data, generate_insights
from .plotting import generate_plot  # Correct function name

# Define the Blueprint for API routes
api = Blueprint('api', __name__)



@api.route('/plot', methods=['POST'])
def plot_stock():
    data = request.get_json()
    if not data or 'ticker' not in data:
        return jsonify({'error': 'Missing ticker in request'}), 400

    ticker = data['ticker']
    period = data.get('period')
    start = data.get('start')
    end = data.get('end')
    plot_type = data.get('plot_type', 'close')
    ma_window = data.get('ma_window') 

    if period and (start or end):
        return jsonify({'error': 'Provide either period or start/end dates, not both'}), 400
    if not period and (not start or not end):
        return jsonify({'error': 'Start and end dates are required when not using period'}), 400

    try:
        if period or ma_window:
            stock_data = load_data(ticker, period=period)
        else:
            stock_data = load_data(ticker, start=start, end=end)

        if stock_data is None or stock_data.empty:
            return jsonify({'error': f'No data found for {ticker}'}), 404

        plot = generate_plot(ticker, stock_data, plot_type, ma_window=ma_window)
        return jsonify({'plot': plot})

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500
    
@api.route('/insights/<ticker>', methods=['GET'])
def get_insights(ticker):
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

        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        # print(ticker, stock_data)
        insights = generate_insights(ticker, stock_data)
        return jsonify(insights)

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500