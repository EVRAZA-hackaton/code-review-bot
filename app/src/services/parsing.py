import io
import tempfile
import zipfile
from pathlib import Path

from app.src.model.constants import FileExtensionEnum
from app.src.model.directory import Directory
from app.src.model.file import File
from app.src.model.project import Project


class ParsingService:
    async def parse(self, file_path: str, file: io.BytesIO) -> Project:
        # Определяем имя файла
        file_name = Path(file_path).name

        # Если файл - ZIP-архив, разбираем содержимое
        if file_name.endswith(".zip"):
            return self._parse_zip(file)
        else:
            return self._parse_single_file(file_name, file)

    def _parse_zip(self, file: io.BytesIO) -> Project:
        """Распаковывает ZIP-архив и создает объект Project."""
        project = Project(dirs=[], files=[])
        with zipfile.ZipFile(
            file, "r"
        ) as zip_ref, tempfile.TemporaryDirectory() as temp_dir:
            zip_ref.extractall(temp_dir)
            temp_dir = Path(temp_dir)

            # Рекурсивно собираем директории и файлы
            project.files = self._parse_files(temp_dir)
            project.dirs = self._parse_directory(temp_dir)

        return project

    def _parse_single_file(self, file_name: str, file: io.BytesIO) -> Project:
        """Парсинг одиночного файла."""
        file_data = file.read().decode("utf-8")
        single_file = File(
            name=file_name,
            data=file_data,
            extension=self._get_file_extension(Path(file_name)),
        )
        return Project(dirs=[], files=[single_file])

    def _parse_directory(self, directory_path: Path) -> list[Directory]:
        """Рекурсивный парсинг директории."""
        dirs = []
        for item in directory_path.iterdir():
            if item.is_dir():
                # Если это папка, создаём вложенную структуру
                dirs.append(
                    Directory(
                        dirs=self._parse_directory(item), files=self._parse_files(item)
                    )
                )

        return dirs

    def _parse_files(self, directory_path: Path) -> list[File]:
        """Парсинг файлов в указанной директории."""
        files = []
        for item in directory_path.iterdir():
            if item.is_file():
                files.append(
                    File(
                        name=item.name,
                        data=item.read_text(),
                        extension=self._get_file_extension(item),
                    )
                )
        return files

    def _get_file_extension(self, file_path: Path) -> FileExtensionEnum:
        """Определяет расширение файла."""
        extension = file_path.suffix.lower().strip(".")  # noqa: F841
        return FileExtensionEnum.CODE_FILE
