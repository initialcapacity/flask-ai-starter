import logging
from dataclasses import dataclass
from typing import List

import requests

from starter.result.result import Result, Failure, Success

logger = logging.getLogger(__name__)


@dataclass
class ChatMessage:
    role: str
    content: str


class OpenAIClient:
    def __init__(self, base_url: str, api_key: str, embeddings_model: str, chat_model: str):
        self.base_url = base_url
        self.api_key = api_key
        self.embeddings_model = embeddings_model
        self.chat_model = chat_model

    def fetch_embedding(self, text) -> Result[List[float]]:
        response = requests.post(
            f"{self.base_url}/embeddings",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.embeddings_model,
                "input": text,
                "encoding_format": "float",
            },
        )
        if not response.ok:
            logger.error(f"Received {response.status_code} response from {self.base_url}: {response.text}")
            return Failure("Failed to fetch embedding")

        return Success(response.json()["data"][0]["embedding"])

    def fetch_chat_completion(self, messages: List[ChatMessage]) -> Result[str]:
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.chat_model,
                "messages": [
                    {"role": message.role, "content": message.content}
                    for message in messages
                ]},
        )
        if not response.ok:
            logger.error(f"Received {response.status_code} response from {self.base_url}: {response.text}")
            return Failure("Failed to fetch completion")

        return Success(response.json()["choices"][0]["message"]["content"])
