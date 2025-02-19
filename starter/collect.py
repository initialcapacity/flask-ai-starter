import logging

import sqlalchemy

from starter.ai.chunker import Chunker
from starter.ai.tokenizer import Tokenizer
from starter.database_support.database_template import DatabaseTemplate
from starter.documents.chunks_gateway import ChunksGateway
from starter.documents.document_collector import DocumentCollector
from starter.documents.documents_gateway import DocumentsGateway
from starter.documents.documents_service import DocumentsService
from starter.environment import Environment

env = Environment.from_env()
logging.basicConfig(level=env.root_log_level)
logging.getLogger('starter').setLevel(level=env.starter_log_level)

db = sqlalchemy.create_engine(env.database_url, pool_size=4)
db_template = DatabaseTemplate(db)

documents_gateway = DocumentsGateway(db_template)
chunks_gateway = ChunksGateway(db_template)
chunker = Chunker(tokenizer=Tokenizer("gpt-4o"), limit=6000)
service = DocumentsService(chunker, chunks_gateway, documents_gateway)

collector = DocumentCollector(documents_gateway, service)
collector.collect(env.feeds)
