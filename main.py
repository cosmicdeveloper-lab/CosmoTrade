from divergence import find_divergence
from Ichimoku_cloud import ichimoku_signal
from moving_average import sma_cross
from fibonacci import get_fibo
from telegram_bot import send_if_changed
from rates import get_all_rates, TOP_30_COINS

import time
from dotenv import load_dotenv
import os

load_dotenv()
tel_token = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('CHAT_ID')


def main():
    while True:
        dataframe = get_all_rates(TOP_30_COINS, timeframe=['2h', '4h', '12h', '1d', '3d'])

        send_if_changed(tel_token, chat_id, 'Divergence', find_divergence(dataframe))
        send_if_changed(tel_token, chat_id, 'SMA Cross', sma_cross(dataframe))
        send_if_changed(tel_token, chat_id, 'Fibonacci', get_fibo(dataframe))
        send_if_changed(tel_token, chat_id, 'Ichimoku Cloud', ichimoku_signal(dataframe))
        time.sleep(3600)


if __name__ == '__main__':
    main()
