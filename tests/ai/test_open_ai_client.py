import unittest

import responses

from starter.ai.open_ai_client import OpenAIClient, ChatMessage
from tests.chat_support import chat_response
from tests.embeddings_support import embedding_response, embedding_vector


class TestOpenAIClient(unittest.TestCase):
    def setUp(self):
        self.client = OpenAIClient(
            base_url="https://openai.example.com",
            api_key="some-key",
            embeddings_model="text-embedding-3-small",
            chat_model="gpt-4o",
        )

    @responses.activate
    def test_fetch_embedding(self):
        responses.add(responses.POST, "https://openai.example.com/embeddings", embedding_response(2))

        self.assertEqual(embedding_vector(2), self.client.fetch_embedding("some query"))

    @responses.activate
    def fetch_chat_completion(self):
        responses.add(responses.POST, "https://openai.example.com/chat/completions", chat_response)

        self.assertEqual(
            "Sounds good to me",
            self.client.fetch_chat_completion([
                ChatMessage(role="user", content="Sound good to you?")
            ]),
        )
