import io
from logging import Logger
import asyncio

from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message
from dependency_injector.wiring import Provide, inject

from app.src.core.contrainers import Container, inject_module
from app.src.services.code_review import CodeReviewService

inject_module(__name__)
router: Router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(
        "Привет! Я помогу тебе провести код ревью проекта, "
        "отправь мне файл или zip-архив"
    )


@router.message()
@inject
async def code_review_handler(
    message: Message,
    bot: Bot,
    logger: Logger,
    code_review_service: CodeReviewService = Provide[Container.code_review_service],
):
    if not message.document:
        await message.reply(text="Пожалуйста загрузите файл")
    tg_file = await bot.get_file(message.document.file_id)
    file: io.BytesIO = await bot.download_file(tg_file.file_path)

    code_review_service.code_review_async(
        file_path=tg_file.file_path,
        file=file,
        bot=bot,
        chat_id=message.chat.id,
        msg_id=message.message_id
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text="Документ взять в работу, распознование началось....",
        reply_to_message_id=message.message_id
    )
