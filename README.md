# Real-Time Crypto Pair Tracker with Kalman Smoothing & Z-Score Alerts

This Dash application provides real-time visualization of cryptocurrency prices (BTC, ETH) with comparison, z-score alerts, and Kalman filter smoothing.  
It connects to Binance’s WebSocket API and supports dynamic time-frame selection (1s, 1m, 5m).

## 🚀 Features
- **Live Binance data feed** for BTCUSDT and ETHUSDT pairs.
- **Pair selection:** BTC vs ETH, BTC only, or ETH only.
- **Time frame selection:** 1 second, 1 minute, or 5 minutes.
- **Kalman Filter smoothing** overlay for denoising price signals.
- **Z-Score Calculation and Alert:** Alerts when z-score crosses a custom threshold.
- **Real-time spread & correlation visualization.**

## 🧠 How It Works
1. Streams real-time trade data using Binance’s WebSocket API.
2. Stores tick data in SQLite (`ticks.db`).
3. Updates charts using Dash callbacks every few seconds.
4. Computes rolling correlation, z-score, and applies a Kalman filter for smoothing.

## ⚙️ Installation & Setup

### 1️⃣ Clone the project
```bash
git clone https://github.com/yourusername/crypto-kalman-dashboard.git
cd crypto-kalman-dashboard
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the app
```bash
python app.py
```
Then open http://127.0.0.1:8050 in your browser.

## 🧩 File Structure
```
📁 Gemscap/
 ┣ 📄 app.py              # Main Dash app
 ┣ 📄 requirements.txt    # Dependencies
 ┣ 📄 README.md           # Documentation
 ┗ 📄 ticks.db            # Auto-generated SQLite database
```

## ⚡ Requirements
See `requirements.txt` for Python packages.

## 🧰 Technologies Used
- **Dash & Plotly** – Interactive web dashboard
- **aiohttp** – Asynchronous WebSocket client
- **SQLite** – Lightweight local data storage
- **NumPy & Pandas** – Data processing
- **pandas_ta / pykalman** – Statistical & Kalman filter tools

## 📊 Future Enhancements
- Add auto-refresh toggle
- Add more crypto pairs dynamically
- Include volatility and hedge ratio charts

---
**Author:** Ganesh  
