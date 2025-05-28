from apscheduler.schedulers.background import BackgroundScheduler
from telegram_bot import send_signals, reset_redis
from config import setup_logger
from app.app import app


def main():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_signals, 'interval', hours=1)
    scheduler.add_job(reset_redis, 'interval', weeks=1)
    scheduler.start()
    app.run('0.0.0.0', 5000)


if __name__ == '__main__':
    main()
