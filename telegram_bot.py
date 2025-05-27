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


def format_msg(name, new_signals):
    lines = set()

    if new_signals:
        for value in new_signals.values():
            logger.info(f'{value} is new')
            lines.add(f'🦉 {value}')
            r.sadd(name, value)

    if lines:
        message_body = '\n'.join(lines)
        message = f"\n📌 *{name}*\n{message_body}"
        send_telegram_message(TOKEN, CHAT_ID, message)

    else:
        logger.info('No new signals.')


SIGNALS_KEY = 'signals_key'
last_reset_time = time.time()


RESET_INTERVAL_SECONDS = 168 * 60 * 60


def filter_data(name, new_data):
    """
    This function prevent repetitive signals
    and update the redis key set
    Reset all the signals every week
    """
    global last_reset_time
    current_time = time.time()

    if current_time - last_reset_time > RESET_INTERVAL_SECONDS:
        r.delete(SIGNALS_KEY)
        r.delete(name)
        last_reset_time = current_time
        logger.info('Signal memory cleared after a week.')

    if new_data is not None:
        sent_signals = r.smembers(SIGNALS_KEY)

        new_signals = {}

        for signal_key, signal_value in new_data.items():
            signal_key_str = str(signal_key)

            if signal_key_str not in sent_signals:
                new_signals[signal_key_str] = signal_value
                r.sadd(SIGNALS_KEY, signal_key_str)
        format_msg(name, new_signals)


def send_signals():
    while True:
        dataframe = get_all_rates()
        filter_data('Divergence', find_divergence(dataframe))
        filter_data('SMA Cross', sma_cross(dataframe))
        filter_data('Fibonacci', get_fibo(dataframe))
        filter_data('Ichimoku Cloud', ichimoku_signal(dataframe))
        time.sleep(3600)
