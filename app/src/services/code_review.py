import io
from aiogram.types import BufferedInputFile

from app.src.services.classifier import ClassifierService
from app.src.services.exporter import ExporterService
from app.src.services.parsing import ParsingService
from app.src.services.sender import SenderService

class CodeReviewService:
    def __init__(
        self,
        parsing_service: ParsingService,
        classifier_service: ClassifierService,
        sender_service: SenderService,
        exporter_service: ExporterService,
    ):
        self.parsing_service = parsing_service
        self.classifier_service = classifier_service
        self.sender_service = sender_service
        self.exporter_service = exporter_service

    async def code_review(self, file_path: str, file: io.BytesIO) -> BufferedInputFile:
        project = await self.parsing_service.parse(file_path=file_path, file=file)
        classified_items = await self.classifier_service.classify(project)
        answers = await self.sender_service.send(classified_items)
        file = await self.exporter_service.export_to_markdown(answers)
        return file
