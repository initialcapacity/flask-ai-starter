from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from sqlalchemy import Connection

from starter.database_support.database_template import DatabaseTemplate
from starter.database_support.result_mapping import map_one_result


@dataclass
class ChunkRecord:
    id: UUID
    document_id: UUID
    content: str


class ChunksGateway:
    def __init__(self, template: DatabaseTemplate):
        self.template = template

    def create(self, document_id: UUID, content: str, connection: Optional[Connection] = None) -> UUID:
        result = self.template.query(
            "insert into chunks (document_id, content) values (:document_id, :content) returning id",
            connection,
            document_id=document_id,
            content=content,
        )

        return map_one_result(result, lambda row: row["id"])

    def find(self, id: UUID, connection: Optional[Connection] = None) -> Optional[ChunkRecord]:
        result = self.template.query(
            "select id, document_id, content from chunks where id = :id",
            connection,
            id=id,
        )

        return map_one_result(result, lambda row: ChunkRecord(
            id=row["id"],
            document_id=row["document_id"],
            content=row["content"]
        ))
