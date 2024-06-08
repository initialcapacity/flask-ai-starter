from unittest import TestCase

import sqlalchemy

from starter.database_support.database_template import DatabaseTemplate
from starter.health_api import health_api
from tests.blueprint_test_support import test_client
from tests.db_test_support import TestDatabaseTemplate


class TestHealthApi(TestCase):
    def test_health_up(self):
        db_template = TestDatabaseTemplate()

        client = test_client(health_api(db_template))

        response = client.get('/health')

        self.assertEqual(200, response.status_code)
        self.assertEqual({'status': 'UP', 'database': 'UP'}, response.json)

    def test_health_down(self):
        db = sqlalchemy.create_engine(
            url='postgresql://localhost:5432/not_there',
            pool_size=4
        )

        client = test_client(health_api(DatabaseTemplate(db)))

        response = client.get('/health')

        self.assertEqual(504, response.status_code)
        self.assertEqual({'status': 'DOWN', 'database': 'DOWN'}, response.json)
