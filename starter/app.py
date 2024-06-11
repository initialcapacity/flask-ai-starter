import logging

import sqlalchemy
from flask import Flask

from starter.ai.open_ai_client import OpenAIClient
from starter.database_support.database_template import DatabaseTemplate
from starter.documents.chunks_gateway import ChunksGateway
from starter.documents.documents_gateway import DocumentsGateway
from starter.environment import Environment
from starter.health_api import health_api
from starter.index_page import index_page
from starter.query.query_service import QueryService
from starter.search.chunks_search_service import ChunksSearchService
from starter.search.embeddings_gateway import EmbeddingsGateway

logger = logging.getLogger(__name__)


def create_app(env: Environment = Environment.from_env()) -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = env.database_url

    db = sqlalchemy.create_engine(env.database_url, pool_size=4)
    db_template = DatabaseTemplate(db)

    documents_gateway = DocumentsGateway(db_template)
    chunks_gateway = ChunksGateway(db_template)
    embeddings_gateway = EmbeddingsGateway(db_template)
    ai_client = OpenAIClient(
        base_url=env.open_ai_base_url,
        api_key=env.open_ai_key,
        embeddings_model="text-embedding-3-small",
        chat_model="gpt-4o"
    )
    chunks_search_service = ChunksSearchService(embeddings_gateway, chunks_gateway, documents_gateway, ai_client)

    query_service = QueryService(chunks_search_service, ai_client)
    app.register_blueprint(index_page(query_service))
    app.register_blueprint(health_api(db_template))

    return app
