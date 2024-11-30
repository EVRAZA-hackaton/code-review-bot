from enum import StrEnum, auto


class FileExtensionEnum(StrEnum):
    CODE_FILE = auto()
    CONFIGURATION_FILE = auto()


class PromptEnum(StrEnum):
    """Determines which prompy suite to use for a single file"""
    CODE_PROMPT = auto()
    CONFIG_PROMPT = auto()
    PROJECT_STRUCTURE_PROMPT = auto()
