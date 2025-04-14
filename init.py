from divergence import find_divergence
from Ichimoku_cloud import ichimoku_signal
from moving_average import sma_cross
from fibonacci import get_fibo
from telegram_bot import send_telegram_message, format_signal_dict, send_if_changed
from rates import get_all_rates, TOP_30_COINS

import time
from dotenv import load_dotenv
import os

load_dotenv()
tel_token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("CHAT_ID")

dataframe = get_all_rates(TOP_30_COINS, timeframe=['1h', '4h', '1d'])

message = '\n------\n'.join([
    format_signal_dict("Divergence", find_divergence(dataframe)),
    format_signal_dict("Ichimoku", ichimoku_signal(dataframe)),
    format_signal_dict("SMA Cross", sma_cross(dataframe)),
    format_signal_dict("Fibonacci", get_fibo(dataframe))
])


if __name__ == '__main__':
    print('Bot started...')
    while True:
        send_if_changed(tel_token, chat_id, message)
        time.sleep(3600)
