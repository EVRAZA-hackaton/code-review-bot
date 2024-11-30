from app.src.services.classifier import ClassifierService
from app.src.services.parsing import ParsingService
from app.src.services.pdf import PDFService
from app.src.services.sender import SenderService


class CodeReviewService:
    def __init__(
        self,
        parsing_service: ParsingService,
        classifier_service: ClassifierService,
        sender_service: SenderService,
        pdf_service: PDFService,
    ):
        self.parsing_service = parsing_service
        self.classifier_service = classifier_service
        self.sender_service = sender_service
        self.pdf_service = pdf_service

    async def code_review(self):
        ...
