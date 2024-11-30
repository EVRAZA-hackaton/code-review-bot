import io
from logging import Logger

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

    await code_review_service.code_review(file_path=tg_file.file_path, file=file)

    return message.reply(text="done")
