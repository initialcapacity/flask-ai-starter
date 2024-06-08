from unittest import TestCase

import responses

from starter.ai.chunker import Chunker
from starter.ai.tokenizer import Tokenizer
from starter.documents.chunks_gateway import ChunksGateway
from starter.documents.document_collector import DocumentCollector
from starter.documents.documents_gateway import DocumentsGateway
from starter.documents.documents_service import DocumentsService
from tests.db_test_support import TestDatabaseTemplate
from tests.rss_support import rss_feed


class TestDocumentCollector(TestCase):
    def setUp(self):
        super().setUp()
        self.db = TestDatabaseTemplate()
        self.db.clear()

        self.documents_gateway = DocumentsGateway(self.db)
        self.chunks_gateway = ChunksGateway(self.db)
        self.chunker = Chunker(tokenizer=Tokenizer("gpt-4o"), limit=30)
        self.service = DocumentsService(self.chunker, self.chunks_gateway, self.documents_gateway)

        self.collector = DocumentCollector(self.documents_gateway, self.service)

    @responses.activate
    def test_collect(self):
        responses.add(responses.GET, "https://rss.example.com", rss_feed)
        responses.add(responses.GET, "https://rss.example.com/1", """<html lang="en"><p>Some text 1</p></html>""")
        responses.add(responses.GET, "https://rss.example.com/2", """<html lang="en"><p>Some text 2</p></html>""")
        self.service.create("https://rss.example.com/2", "Already saved")

        self.collector.collect(["https://rss.example.com"])

        result = self.db.query_to_dict("select source, content from documents")
        self.assertCountEqual([
            {"source": "https://rss.example.com/1", "content": "Some text 1"},
            {"source": "https://rss.example.com/2", "content": "Already saved"},
        ], result)

        result = self.db.query_to_dict("select content from chunks")
        self.assertCountEqual([
            {"content": "Some text 1"},
            {"content": "Already saved"},
        ], result)
