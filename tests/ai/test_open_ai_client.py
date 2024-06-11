import unittest

import responses

from starter.ai.open_ai_client import OpenAIClient, ChatMessage
from tests.chat_support import chat_response
from tests.embeddings_support import embedding_response, embedding_vector
from tests.logging_support import disable_logging


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

        self.assertEqual(embedding_vector(2), self.client.fetch_embedding("some query").value)

    @disable_logging
    @responses.activate
    def test_fetch_embedding_failure(self):
        responses.add(responses.POST, "https://openai.example.com/embeddings", "bad news", status=400)

        self.assertEqual("Failed to fetch embedding", self.client.fetch_embedding("some query").message)

    @responses.activate
    def test_fetch_chat_completion(self):
        responses.add(responses.POST, "https://openai.example.com/chat/completions", chat_response)

        self.assertEqual(
            "Sounds good to me",
            self.client.fetch_chat_completion([
                ChatMessage(role="user", content="Sound good to you?")
            ]).value,
        )

    @disable_logging
    @responses.activate
    def test_fetch_chat_completion_failure(self):
        responses.add(responses.POST, "https://openai.example.com/chat/completions", "bad news", status=400)

        self.assertEqual(
            "Failed to fetch completion",
            self.client.fetch_chat_completion([
                ChatMessage(role="user", content="Sound good to you?")
            ]).message,
        )
