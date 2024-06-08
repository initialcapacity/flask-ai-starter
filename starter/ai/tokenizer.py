from tiktoken import encoding_for_model


class Tokenizer:
    def __init__(self, model_name: str):
        self.encoder = encoding_for_model(model_name)

    def count_tokens(self, text: str) -> int:
        tokens = self.encoder.encode(text)

        return len(tokens)
