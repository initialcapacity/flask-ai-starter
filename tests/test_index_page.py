import unittest

import responses

from starter.ai.open_ai_client import OpenAIClient
from starter.documents.chunks_gateway import ChunksGateway
from starter.documents.documents_gateway import DocumentsGateway
from starter.index_page import index_page
from starter.query.query_service import QueryService
from starter.search.chunks_search_service import ChunksSearchService
from starter.search.embeddings_gateway import EmbeddingsGateway
from tests.blueprint_test_support import test_client
from tests.chat_support import chat_response
from tests.db_test_support import TestDatabaseTemplate
from tests.embeddings_support import embedding_response, embedding_vector


class TestIndexPage(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.db = TestDatabaseTemplate()
        self.db.clear()

        self.documents_gateway = DocumentsGateway(self.db)
        self.chunks_gateway = ChunksGateway(self.db)
        self.embeddings_gateway = EmbeddingsGateway(self.db)
        ai_client = OpenAIClient(base_url="https://openai.example.com", api_key="some-key",
                                 embeddings_model="text-embedding-3-small", chat_model="gpt-4o")

        chunks_service = ChunksSearchService(self.embeddings_gateway, self.chunks_gateway,
                                             self.documents_gateway, ai_client)

        query_service = QueryService(chunks_service, ai_client)
        self.client = test_client(index_page(query_service))

    def test_index_page(self):
        response = self.client.get("/")

        self.assertEqual(200, response.status_code)
        self.assertIn("What would you like to know?", response.text)

    @responses.activate
    def test_query(self):
        responses.add(responses.POST, "https://openai.example.com/embeddings", embedding_response(1))
        responses.add(responses.POST, "https://openai.example.com/chat/completions", chat_response)

        document_id_1 = self.documents_gateway.create("https://example.com/1", "some_content_1")
        chunk_id_1 = self.chunks_gateway.create(document_id_1, "some_content_1")
        self.embeddings_gateway.create(chunk_id_1, embedding_vector(1))

        response = self.client.post("/", data={"query": "Does that sound good?"})

        self.assertEqual(200, response.status_code)
        self.assertIn("https://example.com/1", response.text)
        self.assertIn("Sounds good to me", response.text)
