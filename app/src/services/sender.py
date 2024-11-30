import typing as tp

import requests

from app.src.model.file import File
from app.src.model.constants import PromptEnum
from app.src.model.prompts import PROMPT_ENUM_TO_PROMPT_VALUE


class SenderService:
    def send(
        self, files_prompts_configurations: list[tuple[File, PromptEnum]]
    ) -> list[tuple[File, str]]:
        http_token = "luFd5RRFwjlJuPmQbsNppm2iPepEsMQQ"

        files_and_responses: list[tuple[File, str]] = []
        for file, prompt_enum in files_prompts_configurations:
            file_content = file.data
            prompt_value: str = PROMPT_ENUM_TO_PROMPT_VALUE[prompt_enum]
            response_for_a_file = self.get_response_from_a_file_with_specific_prompt(
                token=http_token, file_content=file_content, prompt=prompt_value
            )
            files_and_responses.append((file, response_for_a_file))
        return files_and_responses

    def get_response_from_a_file_with_specific_prompt(
        self, token: str, file_content: str, prompt: str, temperature: float = 1.0
    ) -> str:

        model_response = self._get_model_response(
            token=token, prompt=prompt, main_query=file_content, temperature=temperature
        )

        return model_response

    def _split_into_chunks(self, string: str, chunks_num: int = 1):
        """Splits file into chunks"""

        chunks_size = len(string) // chunks_num
        return [string[i : i + chunks_size] for i in range(0, len(string), chunks_size)]

    def _get_model_response(
        self, token: str, prompt: str, main_query: str, temperature: float = 1.0
    ) -> str:
        """Comprises request for a specific file"""
        chunks_num = 1

        while True:
            texts = self._split_into_chunks(string=main_query, chunks_num=chunks_num)
            responses: list[dict[str, tp.Any]] = []
            for chunk in texts:
                model_instruction = {
                    "model": "mistral-nemo-instruct-2407",
                    "messages": [
                        {
                            "role": "system",
                            "content": "Oтвечай на русском языке." + prompt,
                        },
                        {"role": "user", "content": chunk},
                    ],
                    "max_tokens": 1024,
                    "temperature": temperature,
                }

                response = requests.post(
                    url="http://84.201.152.196:8020/v1/completions",
                    headers={
                        "Authorization": token,
                        "Content-Type": "application/json",
                    },
                    json=model_instruction,
                )
                response = response.json()
                responses.append(response)
            try:

                answer = "\n".join(
                    [
                        response["choices"][0]["message"]["content"]
                        for response in responses
                    ]
                )
                return answer

            except KeyError:
                chunks_num += 1
                continue
