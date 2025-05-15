import requests
import time
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def send_telegram_message(token, chat_id, message):
    logging.info('Sending to Telegram...')
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    requests.post(url, data=payload)


def format_signal_dict(signal_dict):
    if signal_dict:
        lines = []
        for _, message in sorted(signal_dict.items()):
            lines.append(f'🦉 {message}')
        return '\n'.join(lines)


sent_signals = set()
last_reset_time = time.time()


def send_if_changed(token, chat_id, name, new_message):
    global sent_signals, last_reset_time
    RESET_INTERVAL_SECONDS = 36 * 60 * 60
    current_time = time.time()

    # Check if the reset interval has passed
    if current_time - last_reset_time > RESET_INTERVAL_SECONDS:
        sent_signals.clear()
        last_reset_time = current_time

        logging.info('Signal memory cleared after 48 hours.')

    # Split message into individual signals
    if new_message is not None:
        new_signals = set(new_message.strip().splitlines())

        # Find only the new signals not already sent
        new_to_send = new_signals - sent_signals

        if new_to_send:
            logging.info('Found new signals.')
            # Compose message of only new signals
            message = f"\n📌 *{name}*\n" + "\n".join(sorted(new_to_send))
            send_telegram_message(token, chat_id, message)
            sent_signals.update(new_to_send)
        else:
            logging.info('No new signals — skipped sending.')
