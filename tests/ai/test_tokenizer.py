import unittest

from starter.ai.tokenizer import Tokenizer


class TestTokenizer(unittest.TestCase):
    def test_count_tokens(self):
        tokenizer = Tokenizer("gpt-4o")

        self.assertEqual(7, tokenizer.count_tokens("This string should have 7 tokens"))
