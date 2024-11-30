import dataclasses

from app.src.model.constants import FileExtensionEnum


@dataclasses.dataclass
class File:
    name: str
    data: str = dataclasses.field(repr=False)
    extension: FileExtensionEnum
