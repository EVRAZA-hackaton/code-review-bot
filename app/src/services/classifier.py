from app.src.model.project import Project


class ClassifierService:
    # TODO: опиши модель (датамодель), в котором ты отдашь данные,
    #  которые примет другой сервис и на основе этих данных
    #  - подберет правильный промпт для каждого файла
    async def classify(self, project: Project):
        ...
