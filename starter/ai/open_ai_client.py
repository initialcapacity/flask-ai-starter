from dataclasses import dataclass
from typing import List

import requests


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

    def fetch_embedding(self, text) -> List[float]:
        result = requests.post(
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

        return result.json()["data"][0]["embedding"]

    def fetch_chat_completion(self, messages: List[ChatMessage]) -> str:
        result = requests.post(
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

        return result.json()["choices"][0]["message"]["content"]
