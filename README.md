# cosmotrade

# 📈 Telegram Crypto Trade Signal Bot

A Python bot that analyzes market data and sends **automated trading signals** (Divergence, Ichimoku Cloud, SMA Cross, Fibonacci levels) directly to a **Telegram chat**.

---

## 🚀 Features

- 📡 Fetches price data for the top 30 coins
- 📊 Runs multiple technical analysis strategies:
  - RSI Divergence
  - Ichimoku Cloud signals
  - Moving Average Crosses
  - Fibonacci levels
- 📤 Sends formatted messages to your Telegram bot
- 🧠 Avoids duplicate signals
- 🐳 Optional Docker support for deployment
- ☁️ VPS-friendly: lightweight & runs 24/7

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

```bash
TELEGRAM_TOKEN=your_bot_token
CHAT_ID=your_chat_id
EXCHANGE=your_exchange_name(coinex, kucoin, binance, ...)
```
### check here for more about the exchanges https://docs.ccxt.com/#/

### 4. Run the Bot (Basic)

```bash
python main.py
```

## 🐳 Run with Docker

### 1. Build the image

```bash
docker build -t cosmotrade .
```

### 2. Run the container

```bash
docker run -d --env-file .env --restart always cosmotrade
```

## 🧑‍💻 Author

### Built by Benjamin Amini — feel free to fork and modify!

