import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.config.config import Config, load_config
from app.config.logger import configure_logger

logger = logging.getLogger(__name__)


async def _start_bot():
    configure_logger()

    logger.info("Starting bot")

    config: Config = load_config()

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp: Dispatcher = Dispatcher()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


def main():
    try:
        asyncio.run(_start_bot())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
