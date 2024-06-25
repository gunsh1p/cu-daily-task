import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    BOT_TOKEN: str = field(metadata={'env_name': 'BOT_TOKEN'})
    ADMINS: list[int] = field(metadata={'env_name': 'ADMINS'})
    DB_HOST: str = field(metadata={'env_name': 'DB_HOST'})
    DB_PORT: int = field(metadata={'env_name': 'DB_PORT'})
    DB_NAME: str = field(metadata={'env_name': 'DB_NAME'})
    DB_USER: str = field(metadata={'env_name': 'DB_USER'})
    DB_PASS: str = field(metadata={'env_name': 'DB_PASS'})

def load_config() -> Config:
    admins = list(map(int, os.environ['ADMINS'].split()))
    return Config(
        BOT_TOKEN=os.environ['BOT_TOKEN'],
        ADMINS=admins,
        DB_HOST=os.environ['DB_HOST'],
        DB_PORT=int(os.environ['DB_PORT']),
        DB_NAME=os.environ['DB_NAME'],
        DB_USER=os.environ['DB_USER'],
        DB_PASS=os.environ['DB_PASS']
    )

config: Config = load_config()