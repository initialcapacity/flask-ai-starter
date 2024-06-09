import unittest

from starter.documents.chunks_gateway import ChunksGateway
from starter.documents.documents_gateway import DocumentsGateway
from starter.search.embeddings_gateway import EmbeddingsGateway
from tests.db_test_support import TestDatabaseTemplate
from tests.embeddings_support import embedding_vector, vector_to_string


class TestEmbeddingsGateway(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.db = TestDatabaseTemplate()
        self.db.clear()

        self.documents_gateway = DocumentsGateway(self.db)
        self.chunks_gateway = ChunksGateway(self.db)
        self.gateway = EmbeddingsGateway(self.db)

    def test_create(self):
        document_id = self.documents_gateway.create("https://example.com", "some_content")
        chunk_id = self.chunks_gateway.create(document_id, "some_content")
        vector = embedding_vector(0)

        id = self.gateway.create(chunk_id, vector)

        result = self.db.query_to_dict("select id, chunk_id, embedding from embeddings")
        self.assertEqual([{
            "id": id,
            "chunk_id": chunk_id,
            "embedding": '[' + vector_to_string(vector) + ']',
        }], result)

    def test_unprocessed_chunk_ids(self):
        document_id = self.documents_gateway.create("https://example.com", "some_content")
        chunk_id_1 = self.chunks_gateway.create(document_id, "some_content_1")
        chunk_id_2 = self.chunks_gateway.create(document_id, "some_content_1")
        self.gateway.create(chunk_id_1, embedding_vector(0))

        ids = self.gateway.unprocessed_chunk_ids()

        self.assertEqual([chunk_id_2], ids)

    def find_similar_chunk_id(self):
        document_id = self.documents_gateway.create("https://example.com", "some_content")
        chunk_id_1 = self.chunks_gateway.create(document_id, "some_content_1")
        chunk_id_2 = self.chunks_gateway.create(document_id, "some_content_1")
        self.gateway.create(chunk_id_1, embedding_vector(1))
        self.gateway.create(chunk_id_2, embedding_vector(2))

        self.assertEqual(chunk_id_1, self.gateway.find_similar_chunk_id(embedding_vector(1)))
        self.assertEqual(chunk_id_2, self.gateway.find_similar_chunk_id(embedding_vector(2)))
