from uuid import UUID

from starter.ai.chunker import Chunker
from starter.documents.chunks_gateway import ChunksGateway
from starter.documents.documents_gateway import DocumentsGateway


class DocumentsService:
    def __init__(self, chunker: Chunker, chunks_gateway: ChunksGateway, documents_gateway: DocumentsGateway):
        self.chunker = chunker
        self.chunks_gateway = chunks_gateway
        self.documents_gateway = documents_gateway

    def create(self, source: str, content: str) -> UUID:
        document_id = self.documents_gateway.create(source, content)

        chunks = self.chunker.split(content)
        for chunk in chunks:
            self.chunks_gateway.create(document_id, chunk)

        return document_id
