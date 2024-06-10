import logging

from starter.app import create_app
from starter.environment import Environment

env = Environment.from_env()
logging.basicConfig(level=env.root_log_level)
logging.getLogger('starter').setLevel(level=env.starter_log_level)

if __name__ == '__main__':
    create_app(env).run(debug=env.use_flask_debug_mode, host="0.0.0.0", port=env.port)
