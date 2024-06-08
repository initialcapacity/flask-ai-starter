from typing import Any, List

import sqlalchemy
from sqlalchemy import RowMapping

from starter.database_support.database_template import DatabaseTemplate


class TestDatabaseTemplate(DatabaseTemplate):
    def __init__(self) -> None:
        db = sqlalchemy.create_engine(
            url='postgresql://localhost:5432/ai_starter_test?user=ai_starter&password=ai_starter',
            pool_size=4
        )
        super().__init__(db)

    def clear(self):
        self.query('delete from embeddings')
        self.query('delete from chunks')
        self.query('delete from documents')

    def query_to_dict(self, statement: str, **kwargs: Any) -> List[RowMapping]:
        return [
            row._mapping
            for row in (self.query(statement, **kwargs))
        ]
