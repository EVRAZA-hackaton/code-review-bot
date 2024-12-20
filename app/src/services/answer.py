import io


from aiogram import Bot 

class AnswerService:
    async def answer(self, file: io.BytesIO, chat_id: int, msg_id: int, bot: Bot):
        """Отправляет ответ"""
        await bot.send_document(chat_id=chat_id, document=file, reply_to_message_id=msg_id, caption="Отчет по код-ревью")
    
    async def answer_error(self, chat_id: int, msg_id: int, bot: Bot):
        """Отправляет ответ"""
        await bot.send_message(chat_id=chat_id, reply_to_message_id=msg_id, caption="Что-то пошло не так")
