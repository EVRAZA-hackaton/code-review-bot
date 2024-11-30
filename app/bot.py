import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties

from app.config.config import Config, load_config
from app.config.logger import configure_logger
from app.src.core.contrainers import provide_wire
from app.src.endpoints import code_review

logger = logging.getLogger(__name__)


async def _start_bot():
    configure_logger()
    logger.info("Starting bot")

    config: Config = load_config()
    provide_wire()

    bot: Bot = Bot(
        token=config.tg_bot.token, default=DefaultBotProperties(parse_mode="HTML")
    )
    dp: Dispatcher = Dispatcher()

    dp.include_router(code_review.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, logger=logger)


def main():
    try:
        asyncio.run(_start_bot())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
