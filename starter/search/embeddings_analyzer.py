from starter.ai.open_ai_client import OpenAIClient
from starter.documents.chunks_gateway import ChunksGateway
from starter.search.embeddings_gateway import EmbeddingsGateway


class EmbeddingsAnalyzer:
    def __init__(self,
                 embeddings_gateway: EmbeddingsGateway,
                 chunks_gateway: ChunksGateway,
                 open_ai_client: OpenAIClient):
        self.embeddings_gateway = embeddings_gateway
        self.chunks_gateway = chunks_gateway
        self.open_ai_client = open_ai_client

    def analyze(self):
        chunk_ids = self.embeddings_gateway.unprocessed_chunk_ids()
        for chunk_id in chunk_ids:
            chunk = self.chunks_gateway.find(chunk_id)
            vector = self.open_ai_client.fetch_embedding(chunk.content)
            self.embeddings_gateway.create(chunk_id, vector)
