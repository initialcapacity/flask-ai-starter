import unittest

import responses

from starter.ai.open_ai_client import OpenAIClient
from tests.embeddings_support import embedding_response, embedding_vector


class TestOpenAIClient(unittest.TestCase):
    @responses.activate
    def test_fetch_embedding(self):
        responses.add(
            responses.POST,
            "https://openai.example.com/embeddings",
            embedding_response(2),
        )

        client = OpenAIClient(base_url="https://openai.example.com", api_key="some-key", model="text-embedding-3-small")

        self.assertEqual(
            embedding_vector(2),
            client.fetch_embedding("some query"),
        )
