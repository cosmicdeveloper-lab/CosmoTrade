from telegram_bot import send_signals
from config import setup_logger
from app.app import app
import threading


setup_logger()


def main():
    run_bot = threading.Thread(target=send_signals)
    run_bot.start()
    app.run('0.0.0.0', 5000)


if __name__ == '__main__':
    main()
