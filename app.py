import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import asyncio
import aiohttp
import threading
import time
from pykalman import KalmanFilter
from collections import deque
from datetime import datetime

# ==============================
# Global Data Buffers
# ==============================
maxlen = 300
price_data = {
    "BTCUSDT": deque(maxlen=maxlen),
    "ETHUSDT": deque(maxlen=maxlen)
}

timestamp_data = deque(maxlen=maxlen)

# ==============================
# Dash App
# ==============================
app = dash.Dash(__name__)
app.title = "Dynamic Hedge & Z-Score Monitor"

app.layout = html.Div([
    html.H2("Crypto Hedge Dashboard (BTC-ETH Kalman Filter)", style={"textAlign": "center"}),

    html.Div([
        html.Label("Select Comparison:"),
        dcc.Dropdown(
            id="pair_selector",
            options=[
                {"label": "BTC vs ETH", "value": "BTC_ETH"},
                {"label": "BTC only", "value": "BTC"},
                {"label": "ETH only", "value": "ETH"},
            ],
            value="BTC_ETH",
            style={"width": "40%"}
        ),

        html.Label("Select Timeframe:"),
        dcc.Dropdown(
            id="timeframe_selector",
            options=[
                {"label": "1 Second", "value": "1S"},
                {"label": "1 Minute", "value": "1T"},
                {"label": "5 Minutes", "value": "5T"},
            ],
            value="1S",
            style={"width": "40%"}
        ),

        html.Label("Z-Score Alert Threshold:"),
        dcc.Input(
            id="zscore_threshold",
            type="number",
            value=2.0,
            step=0.1,
            style={"width": "20%"}
        ),
    ], style={"display": "flex", "justifyContent": "space-around"}),

    html.Br(),

    dcc.Graph(id="price_chart"),
    dcc.Graph(id="spread_chart"),
    dcc.Graph(id="zscore_chart"),
    html.Div(id="zscore_alert", style={"textAlign": "center", "fontWeight": "bold", "color": "red"}),

    dcc.Interval(id="update_interval", interval=2000, n_intervals=0)
])

# ==============================
# WebSocket Data Fetch
# ==============================
async def stream_data():
    url = "wss://fstream.binance.com/stream?streams=btcusdt@trade/ethusdt@trade"
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url) as ws:
            async for msg in ws:
                data = msg.json()
                stream = data.get("stream", "")
                payload = data.get("data", {})
                symbol = "BTCUSDT" if "btcusdt" in stream else "ETHUSDT"

                price = float(payload.get("p", 0))
                ts = datetime.utcfromtimestamp(payload.get("T", time.time()) / 1000)

                price_data[symbol].append(price)
                timestamp_data.append(ts)


def start_stream():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(stream_data())


threading.Thread(target=start_stream, daemon=True).start()

# ==============================
# Kalman Filter Function
# ==============================
def kalman_smooth(y):
    if len(y) < 5:
        return np.array(y)
    kf = KalmanFilter(initial_state_mean=0, n_dim_obs=1)
    state_means, _ = kf.filter(y)
    return state_means.flatten()

# ==============================
# Dash Callback
# ==============================
@app.callback(
    [
        Output("price_chart", "figure"),
        Output("spread_chart", "figure"),
        Output("zscore_chart", "figure"),
        Output("zscore_alert", "children")
    ],
    [
        Input("update_interval", "n_intervals"),
        State("pair_selector", "value"),
        State("timeframe_selector", "value"),
        State("zscore_threshold", "value"),
    ]
)
def update_charts(_, pair_choice, tf_choice, z_thresh):
    if not timestamp_data:
        raise dash.exceptions.PreventUpdate

    df = pd.DataFrame({
        "timestamp": list(timestamp_data),
        "BTC": list(price_data["BTCUSDT"]),
        "ETH": list(price_data["ETHUSDT"])
    }).dropna()

    df.set_index("timestamp", inplace=True)
    df = df.resample(tf_choice).last().dropna()

    price_fig = go.Figure()
    spread_fig = go.Figure()
    zscore_fig = go.Figure()
    alert_msg = ""

    if pair_choice == "BTC":
        price_fig.add_trace(go.Scatter(x=df.index, y=df["BTC"], name="BTC", mode="lines", line=dict(color="orange")))
    elif pair_choice == "ETH":
        price_fig.add_trace(go.Scatter(x=df.index, y=df["ETH"], name="ETH", mode="lines", line=dict(color="blue")))
    else:
        # BTC vs ETH
        df["spread"] = df["BTC"] - df["ETH"]
        df["kalman_spread"] = kalman_smooth(df["spread"])
        df["zscore"] = (df["spread"] - df["spread"].mean()) / df["spread"].std()

        price_fig.add_trace(go.Scatter(x=df.index, y=df["BTC"], name="BTC", mode="lines", line=dict(color="orange")))
        price_fig.add_trace(go.Scatter(x=df.index, y=df["ETH"], name="ETH", mode="lines", line=dict(color="blue")))

        spread_fig.add_trace(go.Scatter(x=df.index, y=df["spread"], name="Spread", mode="lines", line=dict(color="gray")))
        spread_fig.add_trace(go.Scatter(x=df.index, y=df["kalman_spread"], name="Kalman Smooth", mode="lines", line=dict(color="green", width=2)))

        zscore_fig.add_trace(go.Scatter(x=df.index, y=df["zscore"], name="Z-Score", mode="lines", line=dict(color="purple")))
        zscore_fig.add_hline(y=z_thresh, line_dash="dash", line_color="red")
        zscore_fig.add_hline(y=-z_thresh, line_dash="dash", line_color="red")

        latest_z = df["zscore"].iloc[-1]
        if abs(latest_z) >= z_thresh:
            alert_msg = f"⚠️ ALERT: |Z|={latest_z:.2f} crossed threshold {z_thresh}"

    # Layout styling
    price_fig.update_layout(title="Price Chart", template="plotly_dark")
    spread_fig.update_layout(title="Spread & Kalman Filter", template="plotly_dark")
    zscore_fig.update_layout(title="Z-Score Chart", template="plotly_dark")

    return price_fig, spread_fig, zscore_fig, alert_msg


# ==============================
# Run App
# ==============================
if __name__ == "__main__":
    print("Starting app...")
    app.run(debug=True)
