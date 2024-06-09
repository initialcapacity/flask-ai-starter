import unittest

import responses

from starter.ai.open_ai_client import OpenAIClient
from starter.documents.chunks_gateway import ChunksGateway
from starter.documents.documents_gateway import DocumentsGateway
from starter.search.chunks_search_service import ChunksSearchService, ChunkSearchResult
from starter.search.embeddings_gateway import EmbeddingsGateway
from tests.db_test_support import TestDatabaseTemplate
from tests.embeddings_support import embedding_vector, embedding_response


class TestChunksSearchService(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.db = TestDatabaseTemplate()
        self.db.clear()

        self.documents_gateway = DocumentsGateway(self.db)
        self.chunks_gateway = ChunksGateway(self.db)
        self.embeddings_gateway = EmbeddingsGateway(self.db)
        ai_client = OpenAIClient(base_url="https://openai.example.com", api_key="some-key",
                                 embeddings_model="text-embedding-3-small", chat_model="gpt-4o")

        self.service = ChunksSearchService(self.embeddings_gateway, self.chunks_gateway, self.documents_gateway, ai_client)

    @responses.activate
    def test_search_for_relevant_chunk(self):
        responses.add(
            responses.POST,
            "https://openai.example.com/embeddings",
            embedding_response(2),
        )

        document_id_1 = self.documents_gateway.create("https://example.com/1", "some_content_1")
        document_id_2 = self.documents_gateway.create("https://example.com/2", "some_content_2")
        chunk_id_1 = self.chunks_gateway.create(document_id_1, "some_content_1")
        chunk_id_2 = self.chunks_gateway.create(document_id_2, "some_content_2")
        self.embeddings_gateway.create(chunk_id_1, embedding_vector(1))
        self.embeddings_gateway.create(chunk_id_2, embedding_vector(2))

        result = self.service.search_for_relevant_chunk("some query")

        self.assertEqual(
            ChunkSearchResult(
                content="some_content_2",
                source="https://example.com/2",
            ),
            result,
        )
