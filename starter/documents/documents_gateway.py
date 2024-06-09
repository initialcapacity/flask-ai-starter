from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from sqlalchemy import Connection

from starter.database_support.database_template import DatabaseTemplate
from starter.database_support.result_mapping import map_one_result


@dataclass
class DocumentRecord:
    id: UUID
    source: str
    content: str


class DocumentsGateway:
    def __init__(self, template: DatabaseTemplate):
        self.template = template

    def create(self, source: str, content: str, connection: Optional[Connection] = None) -> UUID:
        result = self.template.query(
            "insert into documents (source, content) values (:source, :content) returning id",
            connection,
            source=source,
            content=content,
        )

        return map_one_result(result, lambda row: row["id"])

    def exists(self, source: str, connection: Optional[Connection] = None) -> bool:
        result = self.template.query(
            "select count(1) as count from documents where source = :source",
            connection,
            source=source,
        )

        return map_one_result(result, lambda row: row["count"] > 0)

    def find(self, id: UUID, connection: Optional[Connection] = None) -> DocumentRecord:
        result = self.template.query(
            "select id, source, content from documents where id = :id",
            connection,
            id=id,
        )

        return map_one_result(result, lambda row: DocumentRecord(
            id=row["id"],
            source=row["source"],
            content=row["content"],
        ))
