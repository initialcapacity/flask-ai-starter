import logging

from starter.ai.open_ai_client import OpenAIClient
from starter.documents.chunks_gateway import ChunksGateway
from starter.result.result import is_failure
from starter.search.embeddings_gateway import EmbeddingsGateway

logger = logging.getLogger(__name__)


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
        logger.info(f"Starting analysis for {len(chunk_ids)} chunks")

        for chunk_id in chunk_ids:
            chunk = self.chunks_gateway.find(chunk_id)
            logger.debug(f"Analyzing chunk {chunk.id} of document {chunk.document_id}")
            vector_result = self.open_ai_client.fetch_embedding(chunk.content)
            if is_failure(vector_result):
                logger.error(f"{vector_result.message} (chunk {chunk.id})")
                continue
            self.embeddings_gateway.create(chunk_id, vector_result.value)

        logger.info(f"Finished analysis")
