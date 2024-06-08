import logging
import os

from starter.app import create_app
from starter.environment import Environment

logging.basicConfig(level=os.environ.get('ROOT_LOG_LEVEL', 'INFO'))
logging.getLogger('starter').setLevel(level=os.environ.get('STARTER_LOG_LEVEL', 'INFO'))

env = Environment.from_env()

if __name__ == '__main__':
    create_app(env).run(debug=env.use_flask_debug_mode, host="0.0.0.0", port=env.port)
