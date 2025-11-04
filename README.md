# 📊 Crypto Live Pair Analytics — BTC vs ETH Tracker

A **real-time crypto analytics dashboard** built using **Python Dash**, featuring:
- Live data streaming from **Binance Futures WebSocket**
- **Kalman Filter–based dynamic hedge estimation**
- **Rolling correlation & Z-Score chart**
- **Z-Score threshold alerts**
- Multi-timeframe selection (**1s, 1m, 5m**)
- Options to view **BTC only**, **ETH only**, or **BTC vs ETH comparison**

---

## 🧩 Project Overview

This dashboard visualizes and analyzes **real-time relationships between Bitcoin (BTC) and Ethereum (ETH)** using statistical and filtering techniques.

It continuously:
- Streams price & volume data from Binance
- Stores live data in SQLite
- Computes rolling **correlation**, **Z-Score**, and **Kalman-smoothed spread**
- Displays alerts when Z-Score crosses a chosen threshold

---

## 🧠 Key Features

| Feature | Description |
|----------|--------------|
| **Live Price Charts** | Streams BTC & ETH prices in real-time |
| **Spread Chart** | Displays the spread between BTC and ETH |
| **Z-Score Chart** | Shows statistical deviation of spread |
| **Kalman Filter** | Provides a smoothened, adaptive hedge ratio |
| **Z-Score Alerts** | Visual alert when Z-score exceeds user threshold |
| **Multiple Timeframes** | Switch between 1-second, 1-minute, and 5-minute rolling analyses |
| **Data Modes** | Select between BTC-only, ETH-only, or BTC vs ETH comparison |

---

## 🗂️ Project Structure

```
📦 KothamasuNagaVenkataGanesh_CS22B1089
├── app.py                # Main Dash application
├── requirements.txt      # Required dependencies
├── assets/
│   └── style.css         # Optional CSS styling for Dash
└── README.md             # Documentation
```

> 💡 The `assets/` folder is automatically detected by Dash for styling and assets.  
> You can create it in your GitHub repo by clicking **“Add file → Create new file”** and naming it `assets/style.css`.

---

## 🚀 How to Run the Project

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/kothamasuganesh/KothamasuNagaVenkataGanesh_CS22B1089.git
cd KothamasuNagaVenkataGanesh_CS22B1089
```

### 2️⃣ Install Requirements
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Application
```bash
python app.py
```

### 4️⃣ Open in Browser
```
http://127.0.0.1:8050/
```

---

## 🧮 Technical Stack

- **Frontend:** Dash (Plotly)
- **Backend:** Flask (via Dash)
- **Streaming:** Binance WebSocket API
- **Database:** SQLite3
- **Algorithms:**
  - Rolling correlation
  - Kalman Filter for hedge estimation
  - Z-score normalization

---

## ⚙️ Configuration Parameters

| Parameter | Description | Default |
|------------|--------------|----------|
| `Z-Score Threshold` | Triggers alert when crossed | 2.0 |
| `Time Frame` | Rolling window for correlation/spread | 1 second |
| `Symbols` | Choose BTC, ETH, or BTC vs ETH | BTC vs ETH |

---

## 📈 Example Features in Action

- When Z-score > threshold, alert appears on dashboard.
- Kalman filter smooths noisy spread for better visualization.
- User can dynamically switch between analysis windows.

---

## 📁 requirements.txt

```
dash==2.16.1
plotly==5.22.0
pandas==2.2.2
numpy==1.26.4
statsmodels==0.14.2
pandas_ta==0.3.14b0
aiohttp==3.9.5
flask==3.0.3
dash-bootstrap-components==1.6.0
sqlite3-binary
```

---

## 🧑‍💻 Developer

**Name:** Kothamasu Naga Venkata Ganesh  
**Roll No:** CS22B1089  
**Project:** Crypto Price Analytics — BTC vs ETH with Kalman Filter  
**Repository:** [GitHub Repo Link](https://github.com/kothamasuganesh/KothamasuNagaVenkataGanesh_CS22B1089)

---

## 🧾 License

This project is developed for academic and research purposes.  
© 2025 Kothamasu Naga Venkata Ganesh. All rights reserved.
