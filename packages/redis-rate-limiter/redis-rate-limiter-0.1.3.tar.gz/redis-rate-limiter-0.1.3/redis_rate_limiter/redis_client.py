from redis import Redis

from redis_rate_limiter.exceptions import ConfigError

from .config import settings

wrapper = dict(client=None)


def get_redis_client():
    if wrapper["client"]:
        return wrapper["client"]
    if not settings.redis_url:
        raise ConfigError()
    client = Redis.from_url(settings.redis_url)
    assert client.ping()
    return client


redis_client = get_redis_client()
