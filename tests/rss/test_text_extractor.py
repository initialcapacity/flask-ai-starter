import unittest

import responses

from starter.rss.text_extractor import extract_text
from tests.rss_support import html_page


class TestTextExtractor(unittest.TestCase):
    @responses.activate
    def test_extract_text(self):
        responses.add(responses.GET, "https://news.example.com", html_page)

        result = extract_text("https://news.example.com")

        self.assertEqual("Page title A heading Some text in two paragraphs", result)
