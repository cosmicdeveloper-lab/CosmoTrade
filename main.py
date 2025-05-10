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
        dataframe_4h = dataframe[dataframe['timeframe'] == '4h']
        dataframe_1d = dataframe[dataframe['timeframe'] == '1d']

        combined_data = pd.concat([dataframe_4h, dataframe_1d], axis=0)

        divergence_signal = format_signal_dict(find_divergence(dataframe))
        sma_signal = format_signal_dict( sma_cross(dataframe))
        fibo_signal = format_signal_dict(get_fibo(combined_data))
        ichimoku_cloud_signal = format_signal_dict(ichimoku_signal(combined_data))

        send_if_changed(tel_token, chat_id, 'Divergence', divergence_signal)
        send_if_changed(tel_token, chat_id, 'SMA Cross', sma_signal)
        send_if_changed(tel_token, chat_id, 'Fibonacci', fibo_signal)
        send_if_changed(tel_token, chat_id, 'Ichimoku Cloud', ichimoku_cloud_signal)
        time.sleep(3600)
