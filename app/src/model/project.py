import dataclasses

from app.src.model.directory import Directory
from app.src.model.file import File


@dataclasses.dataclass
class Project:
    """На своем уровне список директорий и список файлов"""

    dirs: list[Directory]
    files: list[File]
