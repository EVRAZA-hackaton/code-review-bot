import io
import dataclasses


@dataclasses
class Task:
    """Задача для создания отчета"""

    user_id: int
    message_id: int
    file: io.BytesIO