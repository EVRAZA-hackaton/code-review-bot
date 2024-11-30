from dataclasses import dataclass

from dotenv import load_dotenv

from .base import getenv


@dataclass
class TelegramBotConfig:
    token: str


@dataclass
class Config:
    tg_bot: TelegramBotConfig
    ai_token: str
    ai_url: str

def load_config() -> Config:
    load_dotenv()

    return Config(tg_bot=TelegramBotConfig(
        token=getenv("BOT_TOKEN")),
        ai_token=getenv("AI_TOKEN"),
        ai_url=getenv("ai_url")
    )
