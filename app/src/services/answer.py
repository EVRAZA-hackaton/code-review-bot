import io


from aiogram import Bot 

class AnswerService:
    def answer(self, file: io.BytesIO, chat_id: int, msg_id: int, bot: Bot):
        """Отправляет ответ"""
        bot.send_document(chat_id=chat_id, document=file, reply_to_message_id=msg_id)