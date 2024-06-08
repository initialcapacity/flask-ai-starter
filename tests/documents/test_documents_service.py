import unittest

from starter.ai.chunker import Chunker
from starter.ai.tokenizer import Tokenizer
from starter.documents.chunks_gateway import ChunksGateway
from starter.documents.documents_service import DocumentsService
from starter.documents.documents_gateway import DocumentsGateway
from tests.db_test_support import TestDatabaseTemplate
from tests.document_support import long_content


class TestDocumentsService(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.db = TestDatabaseTemplate()
        self.db.clear()

        self.documents_gateway = DocumentsGateway(self.db)
        self.chunks_gateway = ChunksGateway(self.db)
        self.chunker = Chunker(tokenizer=Tokenizer("gpt-4o"), limit=30)

        self.service = DocumentsService(self.chunker, self.chunks_gateway, self.documents_gateway)

    def test_create(self):
        document_id = self.service.create("https://example.com", long_content)

        document_result = self.db.query_to_dict("select id, source, content from documents")
        self.assertEqual([{
            "id": document_id,
            "source": "https://example.com",
            "content": long_content
        }], document_result)

        chunks_result = self.db.query_to_dict("select document_id, content from chunks")
        self.assertEqual([
            {"document_id": document_id, "content": "Hello? Hello, Dimitri? Listen, I can't hear too well, do you suppose you could turn the music down just"},
            {"document_id": document_id, "content": "st a little? Oh, that's much better. Yes. Fine, I can hear you now, Dimitri. Clear and plain and coming "},
            {"document_id": document_id, "content": "g through fine. I'm coming through fine too, eh? Good, then. Well then as you say we're both coming thro"},
            {"document_id": document_id, "content": "rough fine. Good. Well it's good that you're fine and I'm fine. I agree with you. It's great to be fine."},
        ], chunks_result)
