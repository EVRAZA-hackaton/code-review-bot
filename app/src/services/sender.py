import typing as tp
import logging

import requests
import aiohttp

from app.src.model.file import File
from app.src.model.constants import PromptEnum
from app.src.model.prompts import PROMPT_ENUM_TO_PROMPT_VALUE
from app.config.config import Config, load_config



logger = logging.getLogger(__name__)
config: Config = load_config()


class SenderService:
    async def send(
        self, files_prompts_configurations: list[tuple[File, PromptEnum]]
    ) -> list[tuple[File, str]]:
        logger.info("Отправили в сеть, ждем ответа")
        # http_token = "luFd5RRFwjlJuPmQbsNppm2iPepEsMQQ"

        files_and_responses: list[tuple[File, str]] = []
        for file, prompt_enum in files_prompts_configurations:
            file_content = file.data
            prompt_value: str = PROMPT_ENUM_TO_PROMPT_VALUE[prompt_enum]
            response_for_a_file = await self.get_response_from_a_file_with_specific_prompt(
                file_content=file_content, prompt=prompt_value)
            if response_for_a_file:
                files_and_responses.append((file, response_for_a_file))
        return files_and_responses

    async def get_response_from_a_file_with_specific_prompt(
        self, file_content: str, prompt: str, temperature: float = 1.0
    ) -> str:
        model_response = await self._get_model_response(
            prompt=prompt, main_query=file_content, temperature=temperature)
        return model_response

    def _split_into_chunks(self, string: str, chunks_num: int = 1):
        """Splits file into chunks"""
        chunks_size = len(string) // chunks_num
        return [string[i : i + chunks_size] for i in range(0, len(string), chunks_size)]

    async def _get_model_response(
        self, prompt: str, main_query: str, temperature: float = 1.0
    ) -> str:
        """Comprises request for a specific file"""
        chunks_num = 1
        if not len(main_query):
            return ""
        
        async with aiohttp.ClientSession() as session:
            while True:
                texts = self._split_into_chunks(string=main_query, chunks_num=chunks_num)
                responses: list[dict[str, tp.Any]] = []
                for chunk in texts:
                    model_instruction = self.__get_model_instruction(
                        prompt=prompt, chunk=chunk, temperature=temperature)

                    response = await self.__send_request(session, model_instruction)

                    # response = requests.post(
                    #     url="http://84.201.152.196:8020/v1/completions",
                    #     headers={
                    #         "Authorization": token,
                    #         "Content-Type": "application/json",
                    #     },
                    #     json=model_instruction,
                    # )
                    # response = response.json()
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

    @staticmethod
    def __get_model_instruction(prompt: str, chunk: str, temperature: float):
        return {
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

    @property
    def __get_headers() -> dict[str, str]:
        """Получаем заголовок"""
        return {
                "Authorization": config.ai_token,
                "Content-Type": "application/json",
            }

    async def __send_request(self, session: aiohttp.ClientSession, model_instruction: dict) -> dict:
        """Отправляем запрос в сеть"""
        async with session.post(
            url=config.ai_url,
            json=model_instruction,
            headers=self.__get_headers
        ) as req:
            return await req.json()
