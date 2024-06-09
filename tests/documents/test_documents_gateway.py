from unittest import TestCase

from starter.documents.documents_gateway import DocumentsGateway, DocumentRecord
from tests.db_test_support import TestDatabaseTemplate


class TestDocumentsGateway(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.db = TestDatabaseTemplate()
        self.db.clear()

        self.gateway = DocumentsGateway(self.db)

    def test_create(self):
        id = self.gateway.create("https://example.com", "some content")

        result = self.db.query_to_dict("select id, source, content from documents")
        self.assertEqual([{
            "id": id,
            "source": "https://example.com",
            "content": "some content"
        }], result)

    def test_exists(self):
        self.gateway.create("https://example.com", "some content")

        self.assertTrue(self.gateway.exists("https://example.com"))
        self.assertFalse(self.gateway.exists("https://not-there.example.com"))

    def test_find(self):
        id = self.gateway.create("https://example.com", "some content")

        record = self.gateway.find(id)

        self.assertEqual(
            DocumentRecord(id, "https://example.com", "some content"),
            record,
        )
