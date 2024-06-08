import unittest

import responses

from starter.rss.link_extractor import extract_links
from tests.rss_support import rss_feed


class TestLinkExtractor(unittest.TestCase):
    @responses.activate
    def test_extract_links(self):
        responses.add(responses.GET, "https://rss.example.com", rss_feed)

        self.assertEqual(
            ["https://rss.example.com/1", "https://rss.example.com/2"],
            extract_links("https://rss.example.com")
        )
