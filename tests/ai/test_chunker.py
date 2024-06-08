import unittest

from starter.ai.chunker import Chunker
from starter.ai.tokenizer import Tokenizer
from tests.document_support import long_content


class TestChunker(unittest.TestCase):
    def test_split(self):
        chunker = Chunker(tokenizer=Tokenizer("gpt-4o"), limit=30)

        chunks = chunker.split(long_content)

        self.assertEqual([
            "Hello? Hello, Dimitri? Listen, I can't hear too well, do you suppose you could turn the music down just",
            "st a little? Oh, that's much better. Yes. Fine, I can hear you now, Dimitri. Clear and plain and coming ",
            "g through fine. I'm coming through fine too, eh? Good, then. Well then as you say we're both coming thro",
            "rough fine. Good. Well it's good that you're fine and I'm fine. I agree with you. It's great to be fine.",
        ], chunks)
