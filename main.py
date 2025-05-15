from divergence import find_divergence
from Ichimoku_cloud import ichimoku_signal
from moving_average import sma_cross
from fibonacci import get_fibo
from telegram_bot import send_if_changed, format_signal_dict
from rates import get_all_rates, TOP_30_COINS

import pandas as pd
import time
from dotenv import load_dotenv
import os

load_dotenv()
tel_token = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('CHAT_ID')

if __name__ == '__main__':
    print('Bot started...')

    while True:
        dataframe = get_all_rates(TOP_30_COINS, timeframe=['1h', '4h', '1d'])

        send_if_changed(tel_token, chat_id, 'Divergence', find_divergence(dataframe))
        send_if_changed(tel_token, chat_id, 'SMA Cross', sma_cross(dataframe))
        send_if_changed(tel_token, chat_id, 'Fibonacci', get_fibo(dataframe))
        send_if_changed(tel_token, chat_id, 'Ichimoku Cloud', ichimoku_signal(dataframe))
        time.sleep(3600)
