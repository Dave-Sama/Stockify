from flask import request, jsonify
from .data import load_data
from .plotting import generate_plot
import json


def init_routes(app):
    @app.route("/api/plot", methods=["POST"])
    def plot_api():
        data = request.get_json()
        ticker = data.get("ticker", "NVDA")
        period = data.get("period", "1mo")
        plot_type = data.get("plot_type", "close")

        try:
            stock_data = load_data(ticker, period)
            plot_json = generate_plot(ticker, stock_data, plot_type=plot_type, date_format="%b %d, %Y")
            return jsonify({"plot": json.loads(plot_json), "error": None})
        except ValueError as e:
            return jsonify({"plot": None, "error": str(e)})