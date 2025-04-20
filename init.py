from divergence import find_divergence
from Ichimoku_cloud import ichimoku_signal
from moving_average import sma_cross
from fibonacci import get_fibo
from telegram_bot import format_signal_dict, send_if_changed
from rates import get_all_rates, TOP_30_COINS

import pandas as pd
import time
from dotenv import load_dotenv
import os

load_dotenv()
tel_token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("CHAT_ID")


if __name__ == '__main__':
    print('Bot started...')

    while True:
        dataframe = get_all_rates(TOP_30_COINS, timeframe=['1h', '4h', '1d'])
        dataframe_4h = dataframe[dataframe['timeframe'] == '4h']
        dataframe_1d = dataframe[dataframe['timeframe'] == '1d']

        combined_data = pd.concat([dataframe_4h, dataframe_1d], axis=0)

        message = '\n------\n'.join([
            format_signal_dict("Divergence", find_divergence(dataframe)),
            format_signal_dict("Ichimoku", ichimoku_signal(combined_data)),
            format_signal_dict("SMA Cross", sma_cross(combined_data)),
            format_signal_dict("Fibonacci", get_fibo(combined_data))
        ])

        send_if_changed(tel_token, chat_id, message)
        time.sleep(3600)
