from app.src.model.constants import PromptEnum

PROMPT_ENUM_TO_PROMPT_VALUE = {
    PromptEnum.CODE_PROMPT: "Проанализируй следующий код на Python. Найди возможные проблемы, включая: ошибки, неэффективные конструкции, нарушение стиля кода или лучшие практики. Если возможно, предложи улучшения",
    PromptEnum.CONFIG_PROMPT: "Проверь конфигурирующий файл на его адекватность и оставь отзывы",
}
