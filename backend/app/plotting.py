import plotly.graph_objects as go
import json
import pandas as pd

DEFAULT_DATE_FORMAT = "%Y-%m-%d"
PLOT_HEIGHT = 800
ONE_DAY_MS = 86400000

def generate_plot(ticker: str, data, plot_type: str = "close", date_format: str = DEFAULT_DATE_FORMAT, ma_window: int = 20) -> dict:
    if data is None or data.empty:
        raise ValueError(f"No valid data provided for {ticker}")

    title = f"{ticker} - {data.index[0].strftime('%Y-%m-%d')} to {data.index[-1].strftime('%Y-%m-%d')}"
    
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
    elif plot_type == "moving_average":
        print("***************************************")
        print("MA window requested: ", ma_window)
        print("Data length: ", len(data))
        print("***************************************")
        
        # Cap the window to the dataset length minus 1 to ensure at least one valid MA
        effective_window = min(ma_window, len(data) - 1)
        if effective_window < 10:  # Minimum window for meaningful MA
            effective_window = 10
            print("Warning: Window too small, set to minimum 10 days")
        
        data['MA'] = data['Close'].rolling(window=effective_window).mean()
        fig = go.Figure()
        # Add candlestick trace
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            name="Candlestick"
        ))
        # Add moving average trace
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['MA'],
            mode='lines',
            name=f'{effective_window}-Day MA',
            line=dict(color='orange')
        ))
        fig.update_layout(
            title=f"{ticker} Moving Average ({effective_window}-Day)",
            yaxis_title="Price (USD)",
            xaxis_rangeslider_visible=True,
            template="plotly_white",
            height=PLOT_HEIGHT,
            xaxis=dict(tickformat=date_format)
        )
    elif plot_type == "volume_weighted":
        data['VWPrice'] = (data['Close'] * data['Volume']) / data['Volume'].sum()
        fig = go.Figure(data=[go.Scatter(
            x=data.index,
            y=data['VWPrice'],
            mode='lines',
            name="Volume-Weighted Price"
        )])
        fig.update_layout(
            title=f"{ticker} Volume-Weighted Price",
            yaxis_title="Weighted Price (USD)",
            template="plotly_white",
            height=PLOT_HEIGHT,
            xaxis=dict(tickformat=date_format)
        )
    else:
        raise ValueError(f"Unsupported plot_type: {plot_type}")
    
    return json.loads(fig.to_json())