import unittest

import responses

from starter.ai.open_ai_client import OpenAIClient
from starter.documents.chunks_gateway import ChunksGateway
from starter.documents.documents_gateway import DocumentsGateway
from starter.query.query_service import QueryService, QueryResponse
from starter.search.chunks_search_service import ChunksSearchService
from starter.search.embeddings_gateway import EmbeddingsGateway
from tests.chat_support import chat_response
from tests.db_test_support import TestDatabaseTemplate
from tests.embeddings_support import embedding_response, embedding_vector
from tests.logging_support import disable_logging


class TestQueryService(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.db = TestDatabaseTemplate()
        self.db.clear()

        self.documents_gateway = DocumentsGateway(self.db)
        self.chunks_gateway = ChunksGateway(self.db)
        self.embeddings_gateway = EmbeddingsGateway(self.db)
        ai_client = OpenAIClient(base_url="https://openai.example.com", api_key="some-key",
                                 embeddings_model="text-embedding-3-small", chat_model="gpt-4o")

        chunks_service = ChunksSearchService(
            self.embeddings_gateway,
            self.chunks_gateway,
            self.documents_gateway,
            ai_client
        )

        self.service = QueryService(chunks_service, ai_client)

    @responses.activate
    def test_fetch_response(self):
        responses.add(responses.POST, "https://openai.example.com/embeddings", embedding_response(2))
        responses.add(responses.POST, "https://openai.example.com/chat/completions", chat_response)

        document_id_1 = self.documents_gateway.create("https://example.com/1", "some_content_1")
        document_id_2 = self.documents_gateway.create("https://example.com/2", "some_content_2")
        chunk_id_1 = self.chunks_gateway.create(document_id_1, "some_content_1")
        chunk_id_2 = self.chunks_gateway.create(document_id_2, "some_content_2")
        self.embeddings_gateway.create(chunk_id_1, embedding_vector(1))
        self.embeddings_gateway.create(chunk_id_2, embedding_vector(2))

        result = self.service.fetch_response("Does that sound good")

        self.assertEqual(
            QueryResponse(source="https://example.com/2", response="Sounds good to me"),
            result.value,
        )

    @disable_logging
    @responses.activate
    def test_fetch_response_embedding_failure(self):
        responses.add(responses.POST, "https://openai.example.com/embeddings", "bad news", status=400)

        result = self.service.fetch_response("Does that sound good")

        self.assertEqual("Unable to fetch response", result.message)

    @disable_logging
    @responses.activate
    def test_fetch_response_chat_failure(self):
        responses.add(responses.POST, "https://openai.example.com/embeddings", embedding_response(1))
        responses.add(responses.POST, "https://openai.example.com/chat/completions", "bad news", status=400)

        document_id_1 = self.documents_gateway.create("https://example.com/1", "some_content_1")
        chunk_id_1 = self.chunks_gateway.create(document_id_1, "some_content_1")
        self.embeddings_gateway.create(chunk_id_1, embedding_vector(1))

        result = self.service.fetch_response("Does that sound good")

        self.assertEqual("Unable to fetch response", result.message)
