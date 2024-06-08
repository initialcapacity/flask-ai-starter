from unittest import TestCase
from uuid import UUID

from starter.documents.chunks_gateway import ChunksGateway, ChunkRecord
from starter.documents.documents_gateway import DocumentsGateway
from tests.db_test_support import TestDatabaseTemplate


class TestChunksGateway(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.db = TestDatabaseTemplate()
        self.db.clear()

        self.documents_gateway = DocumentsGateway(self.db)
        self.gateway = ChunksGateway(self.db)

    def test_create(self):
        document_id = self.documents_gateway.create("https://example.com", "some content")
        id = self.gateway.create(document_id, "some content")

        result = self.db.query_to_dict("select id, document_id, content from chunks")

        self.assertEqual([{
            "id": id,
            "document_id": document_id,
            "content": "some content"
        }], result)

    def test_find(self):
        document_id = self.documents_gateway.create("https://example.com", "some content")
        id = self.gateway.create(document_id, "some content")

        self.assertIsNone(self.gateway.find(UUID("bbaaaadd-5e2e-44d0-9627-060d2b48c7ef")))
        self.assertEqual(
            ChunkRecord(id=id, document_id=document_id, content="some content"),
            self.gateway.find(id)
        )
