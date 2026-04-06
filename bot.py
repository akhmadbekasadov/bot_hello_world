import asyncio
import logging
import sys
from datetime import datetime, date

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot
from dotenv import load_dotenv
import os

import config

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

START_DATE = date.fromisoformat(config.START_DATE)
MOSCOW_TZ = pytz.timezone(config.TIMEZONE)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


async def send_daily_message():
    today = datetime.now(MOSCOW_TZ).date()
    day_number = (today - START_DATE).days + 1
    date_str = today.strftime("%d.%m.%Y")

    text = config.MESSAGE_TEMPLATE.format(
        day=day_number,
        total=config.TOTAL_DAYS,
        date=date_str,
    )

    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHANNEL_ID, text=text)
    logging.info(f"Сообщение отправлено: {text!r}")


async def main():
    # Режим теста: python bot.py --test
    if "--test" in sys.argv:
        logging.info("Тестовый режим: отправляю сообщение прямо сейчас...")
        await send_daily_message()
        return

    scheduler = AsyncIOScheduler(timezone=MOSCOW_TZ)
    scheduler.add_job(
        send_daily_message,
        "cron",
        hour=config.POST_HOUR,
        minute=config.POST_MINUTE,
    )
    scheduler.start()
    logging.info(
        f"Бот запущен. Отправка каждый день в "
        f"{config.POST_HOUR:02d}:{config.POST_MINUTE:02d} по {config.TIMEZONE}"
    )

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
