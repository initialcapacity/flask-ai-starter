"""initial_schema

Revision ID: b843cebc9fc7
Revises: 
Create Date: 2024-06-07 15:32:10.214940

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b843cebc9fc7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    create table documents
    (
        id         uuid primary key                  default gen_random_uuid(),
        source     varchar                  not null,
        content    varchar                  not null,
        created_at timestamp with time zone not null default now()
    );
    grant all privileges on table documents to ai_starter;
    create unique index index_data_source on documents (source);
    
    create table chunks
    (
        id         uuid primary key                  default gen_random_uuid(),
        document_id    uuid references documents (id),
        content    varchar                  not null,
        created_at timestamp with time zone not null default now()
    );
    grant all privileges on table chunks to ai_starter;
    create index index_chunks_document_id on chunks (document_id);
    
    create table embeddings
    (
        id         uuid primary key                  default gen_random_uuid(),
        chunk_id   uuid references chunks (id),
        embedding  vector(3072) not null,
        created_at timestamp with time zone not null default now()
    );
    grant all privileges on table embeddings to ai_starter;
    create index index_embeddings_chunk_id on embeddings (chunk_id);
    """)
