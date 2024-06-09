from typing import List, Optional
from uuid import UUID

from sqlalchemy import Connection

from starter.database_support.database_template import DatabaseTemplate
from starter.database_support.result_mapping import map_results, map_one_result
from starter.search.vector_support import vector_to_string


class EmbeddingsGateway:
    def __init__(self, template: DatabaseTemplate):
        self.template = template

    def create(self, chunk_id: UUID, vector: List[float], connection: Optional[Connection] = None) -> UUID:
        result = self.template.query(
            "insert into embeddings (chunk_id, embedding) values (:chunk_id, :vector) returning id",
            connection,
            chunk_id=chunk_id,
            vector=vector,
        )

        return map_one_result(result, lambda row: row["id"])

    def unprocessed_chunk_ids(self, connection: Optional[Connection] = None) -> List[UUID]:
        result = self.template.query("""
            select chunks.id from chunks
                left join public.embeddings e on chunks.id = e.chunk_id
                where e.id is null""", connection)

        return map_results(result, lambda row: row["id"])

    def find_similar_chunk_id(self, vector: List[float], connection: Optional[Connection] = None) -> UUID:
        result = self.template.query(
            """select e.chunk_id from embeddings e order by e.embedding <=> :vector limit 1""",
            connection,
            vector=vector_to_string(vector),
        )

        return map_one_result(result, lambda row: row["chunk_id"])
