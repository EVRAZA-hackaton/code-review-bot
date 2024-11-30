import io
import asyncio
from aiogram.types import BufferedInputFile
from aiogram import Bot

from app.src.services.classifier import ClassifierService
from app.src.services.exporter import ExporterService
from app.src.services.parsing import ParsingService
from app.src.services.sender import SenderService
from app.src.services.answer import AnswerService

class CodeReviewService:
    def __init__(
        self,
        parsing_service: ParsingService,
        classifier_service: ClassifierService,
        sender_service: SenderService,
        exporter_service: ExporterService,
        answer_service: AnswerService
    ):
        self.parsing_service = parsing_service
        self.classifier_service = classifier_service
        self.sender_service = sender_service
        self.exporter_service = exporter_service
        self.answer_service = answer_service

    async def code_review(self, file_path: str, file: io.BytesIO) -> BufferedInputFile:
        project = await self.parsing_service.parse(file_path=file_path, file=file)
        classified_items = await self.classifier_service.classify(project)
        answers = await self.sender_service.send(classified_items)
        file = await self.exporter_service.export_to_markdown(answers)
        return file

    def code_review_async(self, file_path: str, file: io.BytesIO, bot: Bot, chat_id: int, msg_id: int) -> None:
        """Асинхронно запускаем таску на распознование"""
        event_loop = asyncio.get_event_loop()
        event_loop.create_task(self.__code_review_async(file_path, file, bot, chat_id, msg_id))

    async def __code_review_async(self, file_path: str, file: io.BytesIO, bot: Bot, chat_id: int, msg_id: int):

        project = await self.parsing_service.parse(file_path=file_path, file=file)
        classified_items = await self.classifier_service.classify(project)
        answers = await self.sender_service.send(classified_items)
        file = await self.exporter_service.export_to_markdown(answers)
        self.answer_service.answer(file, chat_id, msg_id, bot)
