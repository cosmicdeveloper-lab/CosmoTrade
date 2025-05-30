import logging
from divergence import find_divergence
from Ichimoku_cloud import ichimoku_signal
from moving_average import sma_cross
from fibonacci import get_fibo
from rates import get_all_rates
from config import wait_for_redis
import time
from dotenv import load_dotenv
import os
import requests

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
    This function prevent repetitive signals
    and update the redis key set
    """
    SIGNALS_KEY = f'{name}_signals_key'

    if new_data is not None:
        sent_signals = r.smembers(SIGNALS_KEY)
        logger.info(f'SENT SIGNALS:{sent_signals}')

        new_signals = {}

        for signal_key, signal_value in new_data.items():
            signal_key_str = str(signal_key)

            if signal_key_str not in sent_signals:
                new_signals[signal_key_str] = signal_value
                r.sadd(SIGNALS_KEY, signal_key_str)
                r.sadd(name, signal_value)
                logger.info(f'Added {signal_key_str} to {SIGNALS_KEY}')
        logger.info(f'New signals: {new_signals}')

        lines = set()

        if new_signals:
            for value in new_signals.values():
                logger.info(f'{value} is new')
                lines.add(f'🦉 {value}')

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
    filter_data('Divergence', find_divergence(dataframe))
    filter_data('SMA Cross', sma_cross(dataframe))
    filter_data('Fibonacci', get_fibo(dataframe))
    filter_data('Ichimoku Cloud', ichimoku_signal(dataframe))
