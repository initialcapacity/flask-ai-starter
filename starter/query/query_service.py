import logging
from dataclasses import dataclass

from starter.ai.open_ai_client import OpenAIClient, ChatMessage
from starter.result.result import is_failure, Result, Failure, Success
from starter.search.chunks_search_service import ChunksSearchService

logger = logging.getLogger(__name__)


@dataclass
class QueryResponse:
    source: str
    response: str


class QueryService:
    def __init__(self, chunks_search_service: ChunksSearchService, ai_client: OpenAIClient):
        self.chunks_search_service = chunks_search_service
        self.ai_client = ai_client

    def fetch_response(self, query: str) -> Result[QueryResponse]:
        chunk_result = self.chunks_search_service.search_for_relevant_chunk(query)
        if is_failure(chunk_result):
            logger.error(f"Unable to fetch relevant chunk for query: {query}")
            return Failure("Unable to fetch response")

        chunk = chunk_result.value
        completion_result = self.ai_client.fetch_chat_completion([
            ChatMessage(role="system", content="You are a reporter for a major world newspaper."),
            ChatMessage(role="system", content="Write your response as if you were writing a short, high-quality news"
                                               "article for your paper. Limit your response to one paragraph."),
            ChatMessage(role="system", content=f"Use the following article for context: {chunk.content}"),
            ChatMessage(role="user", content=query),
        ])
        if is_failure(completion_result):
            logger.error(f"Unable to fetch chat response for query: {query}")
            return Failure("Unable to fetch response")

        return Success(QueryResponse(
            source=chunk.source,
            response=completion_result.value
        ))
