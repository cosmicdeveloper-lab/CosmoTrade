<p align="center">
  <img src="https://drive.google.com/uc?id=1WIAq3KN05TBSeoL7x8Ur5RAnCbyp2PkB" alt="CosmoTrade Logo" width="200"/>
</p>

<h1 align="center">🚀 CosmoTrade</h1>
<h3 align="center">An Automated Crypto Signal Bot for Telegram Using Technical Indicators</h3>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#example-signal">Example</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

---

## 📈 Overview

**CosmoTrade** is a fully automated crypto trading signal bot that analyzes market trends using multiple technical indicators and delivers real-time alerts to your Telegram chat. Designed for crypto traders, developers, and enthusiasts, it supports multiple exchanges and strategies, all while being lightweight and easy to deploy.

---

## 🚀 Features

- 📡 Real-time price data for top 30 cryptocurrencies  
- 🔍 Multiple technical analysis strategies:
  - RSI & MACD Divergence
  - Ichimoku Cloud Breakouts
  - Moving Average Crosses (7/25/99)
  - Fibonacci 0.618 Levels
- 📤 Automatically sends formatted signals to your Telegram bot
- 🪐 Duplicate signal prevention
- 🐳 Docker support for simplified deployment
- ☁️ Lightweight & VPS-friendly (24/7 operation)
- 🧾 Built-in Flask app to view signals and maintain a trading journal

---

## 🧠 Strategy Logic

**Divergence Detection (RSI & MACD):**  
When price movement conflicts with indicator direction (e.g., rising price but falling RSI/MACD), this may indicate an upcoming reversal.

**Ichimoku Cloud Breakouts:**  
Signals are triggered when key Ichimoku components break above or below the cloud, indicating strong buy/sell opportunities.

**Moving Average Crossovers:**  
Bullish: `7 > 25 > 99`  
Bearish: `99 > 25 > 7`

**Fibonacci Retracement (0.618):**  
Monitors price behavior around the 0.618 level, commonly used for reversals or support/resistance.

> ⚠️ **Disclaimer:** This bot is for informational purposes. Always conduct independent market analysis before trading.

---

## 📦 Requirements

- Python 3.8+
- `pip` or Docker
- Telegram Bot Token and Chat ID
- Flask (for journal interface)
- `.env` file with exchange and credentials
- Redis (used as a database/cache)


---

## 🧰 Install Redis

**Redis is required for managing state and caching signals.**

---

### 🖥️ On Ubuntu/Debian:

```bash
sudo apt update
sudo apt install redis-server

sudo systemctl enable redis-server
sudo systemctl start redis-server
```

### 🍎 On macOS (using Homebrew):

```bash
brew install redis
brew services start redis
```

### 🐳 Docker Alternative:

```bash
docker run -d --name redis -p 6379:6379 redis
```
> ⚠️ **Disclaimer:** Make sure Redis is running and accessible before starting the bot..
---

## 🛠️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/cosmicdeveloper-lab/cosmotrade.git
cd cosmotrade
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a .env file
more about the exchanges https://docs.ccxt.com/#/

```bash
TELEGRAM_TOKEN=your_bot_token
CHAT_ID=your_chat_id
EXCHANGE=your_exchange_name(coinex, kucoin, binance, ...)
```

### 4. Run the Bot (Basic)

```bash
python main.py
```

## 🐳 Or Run with Docker

### 1. Clone the repo

```bash
git clone https://github.com/cosmicdeveloper-lab/cosmotrade.git
cd cosmotrade
```

### 2. Build the image

```bash
docker build -t cosmotrade .
```

### 3. Create a .env file
more about the exchanges https://docs.ccxt.com/#/

```bash
TELEGRAM_TOKEN=your_bot_token
CHAT_ID=your_chat_id
EXCHANGE=your_exchange_name(coinex, kucoin, binance, ...)
```

### 4. Run the container
Running constantly and auto restart

```bash
docker run -d --env-file .env --restart always cosmotrade
```

## 📸 Example Signal

Sample output delivered via Telegram:

Routes available: /signals/, /journal/

![CosmoTrade Signal Screenshot](https://drive.google.com/uc?id=1nnmfVOSD7a3ox4nY8n6bsguXqvwVmWJR)

![FLASK JORNAL](https://drive.google.com/uc?id=1ITpNnZ-5R_9eM2cqasAZGUM5RgJHZOby)

![FLASK SIGNALS](https://drive.google.com/uc?id=1-ZvmWb9rmhV29XCbcPRt_v_DjqZASD0P)


## Run tests
```bash
python -m unittest discover tests
```

## 🧑‍💻 Author

### Built by Benjamin Amini — feel free to fork and modify!

## 📄 License

This project is licensed under the [MIT License](./LICENSE).

