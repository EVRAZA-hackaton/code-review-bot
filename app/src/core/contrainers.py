from typing import Set

from dependency_injector import containers, providers

from app.src.services.classifier import ClassifierService
from app.src.services.code_review import CodeReviewService
from app.src.services.parsing import ParsingService
from app.src.services.pdf import PDFService
from app.src.services.sender import SenderService


class Container(containers.DeclarativeContainer):
    parsing_service = providers.Factory(ParsingService)
    classifier_service = providers.Factory(ClassifierService)
    sender_service = providers.Factory(SenderService)
    pdf_service = providers.Factory(PDFService)

    code_review_service = providers.Factory(
        CodeReviewService,
        parsing_service=parsing_service,
        classifier_service=classifier_service,
        sender_service=sender_service,
        pdf_service=pdf_service,
    )


modules: Set = set()
container = Container()


def inject_module(module_name: str):
    modules.add(module_name)


def provide_wire(*wires: list):
    container.wire(modules=modules)
