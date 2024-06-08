import os
from dataclasses import dataclass
from typing import List


@dataclass
class Environment:
    port: int
    database_url: str
    use_flask_debug_mode: bool
    feeds: List[str]

    @classmethod
    def from_env(cls) -> 'Environment':
        return cls(
            port=int(os.environ.get('PORT', 5001)),
            database_url=cls.__require_env('DATABASE_URL'),
            use_flask_debug_mode=os.environ.get('USE_FLASK_DEBUG_MODE', 'false') == 'true',
            feeds=cls.__require_env('FEEDS').strip().split(','),
        )

    @classmethod
    def __require_env(cls, name: str) -> str:
        value = os.environ.get(name)
        if value is None:
            raise Exception(f'Unable to read {name} from the environment')
        return value
