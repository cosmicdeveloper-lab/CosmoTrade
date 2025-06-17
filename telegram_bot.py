import logging
from divergence import find_divergence
from ema import ema_cross
from rates import get_all_rates
from config import wait_for_redis
import time
from dotenv import load_dotenv
import os
import requests
from bollingersi import bollinger_bands

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
logger = logging.getLogger(__name__)
r = wait_for_redis()


def send_telegram_message(token, chat_id, message):
    logging.info('Sending to Telegram...')
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    requests.post(url, data=payload)


def filter_data(name, new_data):
    """
    Prevents duplicate signals by storing seen keys in Redis.
    Sends a Telegram notification only for new signals.
    """
    SIGNALS_KEY = f'{name}_signals_key'
    new_signals = {}

    for signal_key, signal_value in new_data.items():
        signal_key_str = str(signal_key)
        if r.sadd(SIGNALS_KEY, signal_key_str):
            new_signals[signal_key_str] = signal_value
            r.sadd(name, signal_value)

    if new_signals:
        logger.info(f'New signals: {new_signals}')
        lines = {f'🦉 {value}' for value in new_signals.values()}
        message_body = '\n'.join(lines)
        message = f"\n📌 *{name}*\n{message_body}"
        send_telegram_message(TOKEN, CHAT_ID, message)
    else:
        logger.info('No new signals.')


def reset_redis():
    r.delete(SIGNALS_KEY)
    r.delete(name)
    logger.info('Signal memory cleared after a week.')


def send_signals():
    dataframe = get_all_rates()
    dataframe_1d = dataframe[dataframe['timeframe'] == '1d']
    filter_data('EMA Cross', ema_cross(dataframe_1d))
    filter_data('Divergence', find_divergence(dataframe))
    filter_data('Bollingersi', bollinger_bands(dataframe))
