import logging
from divergence import find_divergence
from Ichimoku_cloud import ichimoku_signal
from moving_average import sma_cross
from fibonacci import get_fibo
from rates import get_all_rates
from config import r
import time
from dotenv import load_dotenv
import os
import requests

# LOad telegram data
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')


def send_telegram_message(token, chat_id, message):
    logging.info('Sending to Telegram...')
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    requests.post(url, data=payload)


def format_signal_dict(name, new_signals):
    signals = new_signals
    lines = []
    for signal in signals:
        lines.append(f'🦉 {signal}')
    message_body = '\n'.join(lines)
    message = f"\n📌 *{name}*\n{message_body}"
    send_telegram_message(TOKEN, CHAT_ID, message)


SIGNALS_KEY = 'signals_key'
last_reset_time = time.time()


RESET_INTERVAL_SECONDS = 120 * 60 * 60


def send_if_changed(name, new_data):
    global last_reset_time
    current_time = time.time()

    # Reset sent signals every RESET_INTERVAL_SECONDS (120 hours in this case)
    if current_time - last_reset_time > RESET_INTERVAL_SECONDS:
        r.delete(SIGNALS_KEY)
        r.delete(name)
        last_reset_time = current_time
        logging.info('Signal memory cleared after 72 hours.')

    if new_data is not None:
        # Retrieve sent signals (these will be returned as a set)
        sent_signals = r.smembers(SIGNALS_KEY)

        # Filter new signals: only those keys not in sent_signals.
        new_signals = {str(k): v for k, v in new_data.items() if str(k) not in sent_signals}

        if new_signals:
            # Add signals keys and values to separate reddis sets
            r.sadd(SIGNALS_KEY, *new_signals.keys())
            r.sadd(name, *new_signals.values())
            format_signal_dict(name, new_signals.values())
            logging.info('Signal with new keys: %s', list(new_signals.keys()))
        else:
            logging.info('No new signals.')


def send_signals():
    while True:
        dataframe = get_all_rates()
        send_if_changed('Divergence', find_divergence(dataframe))
        send_if_changed('SMA Cross', sma_cross(dataframe))
        send_if_changed('Fibonacci', get_fibo(dataframe))
        send_if_changed('Ichimoku Cloud', ichimoku_signal(dataframe))
        time.sleep(3600)
