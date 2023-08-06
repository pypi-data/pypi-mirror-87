class RateLimitExceeded(Exception):
    pass


class ConfigError(Exception):
    def __str__(self):
        return "No Redis URL Config"
