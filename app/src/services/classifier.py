from app.src.model.project import Project
from app.src.model.directory import Directory
from app.src.model.file import File
from app.src.model.constants import PromptEnum, FileExtensionEnum


class ClassifierService:

    def _parse_dir(
        self, directory: Directory | Project
    ) -> list[tuple[File, PromptEnum]]:

        current_level_files: list[File] = directory.files

        current_level_files_enums: list[tuple[File, PromptEnum]] = []

        for file in current_level_files:
            file_global_extension = file.extension

            match file_global_extension:
                case FileExtensionEnum.CODE_FILE:
                    prompt_enum: PromptEnum = PromptEnum.CODE_PROMPT
                case FileExtensionEnum.CONFIGURATION_FILE:
                    prompt_enum = PromptEnum.CONFIG_PROMPT

            current_level_files_enums.append((file, prompt_enum))

        for next_level_dir in directory.dirs:
            current_level_files_enums.extend(self._parse_dir(next_level_dir))

        return current_level_files_enums

    def classify(self, project: Project) -> list[tuple[File, PromptEnum]]:
        return self._parse_dir(project)
