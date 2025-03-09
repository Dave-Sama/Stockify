import json
import plotly.graph_objects as go

DEFAULT_DATE_FORMAT = "%Y-%m-%d"
PLOT_HEIGHT = 800
ONE_DAY_MS = 86400000


def generate_plot(ticker: str, data, plot_type: str = "close", date_format: str = DEFAULT_DATE_FORMAT) -> dict:
    if data is None or data.empty:
        raise ValueError(f"No valid data provided for {ticker}")
    title = f"{ticker} - {data.index[0].strftime('%Y-%m-%d')} to {data.index[-1].strftime('%Y-%m-%d')}"
    print(data)
    print(data.index[-1])
    print(data.index[0])
    if plot_type == "close":
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            name="Candlestick"
        )])
        fig.update_layout(
            title=title,
            yaxis_title="Price (USD)",
            xaxis_rangeslider_visible=True,
            template="plotly_white",
            height=PLOT_HEIGHT,
            xaxis=dict(tickformat=date_format)
        )
    elif plot_type == "volume":
        fig = go.Figure(data=[go.Bar(
            x=data.index,
            y=data["Volume"],
            name="Volume",
            marker_color="teal"
        )])
        fig.update_layout(
            title=f"{ticker} Volume",
            yaxis_title="Volume",
            xaxis_rangeslider_visible=True,
            template="plotly_white",
            height=PLOT_HEIGHT,
            xaxis=dict(tickformat=date_format)
        )
    return json.loads(fig.to_json())  # Return dict instead of string