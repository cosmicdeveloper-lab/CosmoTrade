<p align="center">
  <img src="assets/logo_cosmotrade.jpg" alt="CosmoTrade Logo" width="300"/>
</p>

<h1 align="center">CosmoTrade</h1>
<p align="center">📈 Telegram Crypto Trade Signal Bot</p>


# CosmoTrade

## 📈 Telegram Crypto Trade Signal Bot

- CosmoTrade is an automated crypto trading signal bot that uses multiple technical indicators to send real-time alerts to Telegram. Ideal for crypto enthusiasts, traders, and developers.
---

## 🚀 Features

- 📡 Fetches price data for the top 30 coins
- 📊 Runs multiple technical analysis strategies:
  - RSI & MACD Divergence
  - Ichimoku Cloud signals
  - Moving Average Crosses
  - Fibonacci 0.618 level
- 📤 Sends formatted messages to your Telegram bot
- 🪐 Avoids duplicate signals
- 🐳 Optional Docker support for deployment
- ☁️ VPS-friendly: lightweight & runs 24/7

---
## 🧠 Logic

- Divergence (RSI & MACD):
    - A divergence occurs when the price moves in one direction while indicators like RSI and MACD move in the opposite direction. For example, if the price rises but RSI and MACD fall, this can signal a potential reversal.

- Ichimoku Cloud:
    - When the lagging span, conversion line, base line, and price all break out of the Ichimoku Cloud (either above or below), it may indicate a strong trading signal—above the cloud suggests a buy signal, below suggests a sell signal.

- Moving Average Crosses:
    - When short-term (7), mid-term (25), and long-term (99) moving averages cross in a specific order (e.g., 7 > 25 > 99), it often signals a bullish trend. Conversely, 99 > 25 > 7 indicates a bearish trend.

- Fibonacci Level (0.618):
    - The 0.618 Fibonacci retracement level is a commonly watched point of resistance or support. Price reactions around this level can suggest potential reversals or continuation.

- ⚠️ Caution:
  - These are not guaranteed signals. Always verify and analyze the market independently before making any trading decisions.

---

## 📦 Requirements

- Python 3.8+
- Telegram bot token + chat ID
- Optional: Docker (for containerized setup)

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

Here's what a typical signal looks like in Telegram:

![CosmoTrade Signal Screenshot](assets/example.jpg)

## 🧑‍💻 Author

### Built by Benjamin Amini — feel free to fork and modify!

