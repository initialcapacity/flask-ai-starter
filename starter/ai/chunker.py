from typing import List

from starter.ai.tokenizer import Tokenizer


class Chunker:
    def __init__(self, tokenizer: Tokenizer, limit: int):
        self.tokenizer = tokenizer
        self.limit = limit

    def split(self, text: str) -> List[str]:
        token_count = self.tokenizer.count_tokens(text)
        overlap = int(self.limit / 30)
        midpoint = int(len(text) / 2)

        if token_count < self.limit:
            return [text]
        else:
            first_part = text[:midpoint + overlap]
            second_part = text[midpoint - overlap:]

            return self.split(first_part) + self.split(second_part)
