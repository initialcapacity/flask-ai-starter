import logging

import sqlalchemy
from flask import Flask

from starter.database_support.database_template import DatabaseTemplate
from starter.environment import Environment
from starter.health_api import health_api

logger = logging.getLogger(__name__)


def create_app(env: Environment = Environment.from_env()) -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = env.database_url

    db = sqlalchemy.create_engine(env.database_url, pool_size=4)
    db_template = DatabaseTemplate(db)

    app.register_blueprint(health_api(db_template))

    return app
