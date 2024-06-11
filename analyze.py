import logging

import sqlalchemy

from starter.ai.open_ai_client import OpenAIClient
from starter.database_support.database_template import DatabaseTemplate
from starter.documents.chunks_gateway import ChunksGateway
from starter.environment import Environment
from starter.search.embeddings_analyzer import EmbeddingsAnalyzer
from starter.search.embeddings_gateway import EmbeddingsGateway

env = Environment.from_env()
logging.basicConfig(level=env.root_log_level)
logging.getLogger('starter').setLevel(level=env.starter_log_level)

db = sqlalchemy.create_engine(env.database_url, pool_size=4)
db_template = DatabaseTemplate(db)

chunks_gateway = ChunksGateway(db_template)
embeddings_gateway = EmbeddingsGateway(db_template)
ai_client = OpenAIClient(
    base_url=env.open_ai_base_url,
    api_key=env.open_ai_key,
    embeddings_model="text-embedding-3-small",
    chat_model="gpt-4o"
)

analyzer = EmbeddingsAnalyzer(embeddings_gateway, chunks_gateway, ai_client)
analyzer.analyze()
