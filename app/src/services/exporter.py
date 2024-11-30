import io

from aiogram.types import BufferedInputFile

from app.src.model.file import File


class ExporterService:
    async def export_to_markdown(
        self, answers: list[tuple[File, str]]
    ) -> BufferedInputFile:
        # Сохраняем в BytesIO
        file_buffer = io.BytesIO()

        for file, data in answers:
            file_name = f"# {file.file_path}\n"
            file_buffer.write(file_name.encode("utf-8"))
            file_buffer.write(data.encode("utf-8"))
            file_buffer.write("\n\n".encode("utf-8"))

        file_buffer.seek(0)  # Возвращаем курсор в начало файла

        # Отправляем файл обратно
        markdown_file = BufferedInputFile(file_buffer.read(), filename="Report.md")
        return markdown_file
