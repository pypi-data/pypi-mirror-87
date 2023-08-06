import socket
from dataclasses import dataclass, field


@dataclass
class Settings:
    redis_url: str = ""
    key_prefix: str = field(default_factory=socket.gethostname)


settings = Settings()


def basic_config(redis_url: str = "", key_prefix: str = ""):
    if redis_url:
        settings.redis_url = redis_url
    if key_prefix:
        settings.key_prefix = key_prefix