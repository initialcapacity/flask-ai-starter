import unittest

import responses

from starter.ai.open_ai_client import OpenAIClient
from starter.documents.chunks_gateway import ChunksGateway
from starter.documents.documents_gateway import DocumentsGateway
from starter.search.embeddings_analyzer import EmbeddingsAnalyzer
from starter.search.embeddings_gateway import EmbeddingsGateway
from starter.search.vector_support import vector_to_string
from tests.db_test_support import TestDatabaseTemplate
from tests.embeddings_support import embedding_response, embedding_vector


class TestEmbeddingsAnalyzer(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.db = TestDatabaseTemplate()
        self.db.clear()

        self.documents_gateway = DocumentsGateway(self.db)
        self.chunks_gateway = ChunksGateway(self.db)
        embeddings_gateway = EmbeddingsGateway(self.db)
        ai_client = OpenAIClient(base_url="https://openai.example.com", api_key="some-key",
                                 embeddings_model="text-embedding-3-small", chat_model="gpt-4o")

        self.analyzer = EmbeddingsAnalyzer(embeddings_gateway, self.chunks_gateway, ai_client)

    @responses.activate
    def test_analyze(self):
        responses.add(responses.POST, "https://openai.example.com/embeddings", embedding_response(2))
        document_id = self.documents_gateway.create("https://example.com", "some_content")
        chunk_id_1 = self.chunks_gateway.create(document_id, "some_content_1")
        chunk_id_2 = self.chunks_gateway.create(document_id, "some_content_1")

        self.analyzer.analyze()

        result = self.db.query_to_dict("select chunk_id, embedding from embeddings")
        self.assertCountEqual([{
            "chunk_id": chunk_id_1,
            "embedding": vector_to_string(embedding_vector(2)),
        }, {
            "chunk_id": chunk_id_2,
            "embedding": vector_to_string(embedding_vector(2)),
        }], result)
