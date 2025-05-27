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

# LOad telegram data
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
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


SIGNALS_KEY = 'signals_key'
last_reset_time = time.time()


RESET_INTERVAL_SECONDS = 72 * 60 * 60


def send_if_changed(name, new_data):
    global last_reset_time
    current_time = time.time()
    lines = []

    # Reset sent signals every RESET_INTERVAL_SECONDS (72 hours in this case)
    if current_time - last_reset_time > RESET_INTERVAL_SECONDS:
        r.delete(SIGNALS_KEY)
        r.delete(name)
        last_reset_time = current_time
        logging.info('Signal memory cleared after 120 hours.')

    if new_data is not None:
        seen_signals = r.smembers(name)
        for signal_key, signal_value in new_data.items():
            signal_key_str = str(signal_key)

            if not r.sismember(SIGNALS_KEY, signal_key_str):
                if signal_value not in seen_signals:
                    lines.append(f'🦉 {signal_value}')
                    r.sadd(SIGNALS_KEY, signal_key_str)
                    r.sadd(name, signal_value)
                    logging.info("SIGNALS_KEY members: %s", r.smembers(SIGNALS_KEY))
                    logging.info("%s members: %s", name, r.smembers(name))

        if lines:
            message_body = '\n'.join(lines)
            message = f"\n📌 *{name}*\n{message_body}"
            send_telegram_message(TOKEN, CHAT_ID, message)
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
