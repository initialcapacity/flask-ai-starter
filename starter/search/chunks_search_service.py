from dataclasses import dataclass

from starter.ai.open_ai_client import OpenAIClient
from starter.documents.chunks_gateway import ChunksGateway
from starter.documents.documents_gateway import DocumentsGateway
from starter.search.embeddings_gateway import EmbeddingsGateway


@dataclass
class ChunkSearchResult:
    content: str
    source: str


class ChunksSearchService:
    def __init__(self,
                 embeddings_gateway: EmbeddingsGateway,
                 chunks_gateway: ChunksGateway,
                 documents_gateway: DocumentsGateway,
                 open_ai_client: OpenAIClient):
        self.embeddings_gateway = embeddings_gateway
        self.chunks_gateway = chunks_gateway
        self.documents_gateway = documents_gateway
        self.open_ai_client = open_ai_client

    def search_for_relevant_chunk(self, query: str) -> ChunkSearchResult:
        vector = self.open_ai_client.fetch_embedding(query)
        chunk_id = self.embeddings_gateway.find_similar_chunk_id(vector)
        chunk = self.chunks_gateway.find(chunk_id)
        document = self.documents_gateway.find(chunk.document_id)

        return ChunkSearchResult(
            content=chunk.content,
            source=document.source,
        )
