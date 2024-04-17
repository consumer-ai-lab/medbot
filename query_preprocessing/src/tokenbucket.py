from redis import Redis
from .redis_manager import get_redis_manager
class TokenBucket:
    def __init__(self, redis_manager: Redis, key, size_of_bucket) -> None:
        self.redis_manager = redis_manager
        self.key = key
        self.size_of_bucket = size_of_bucket
        self.refill()
    
    def consume(self):
        self.redis_manager.lpop(self.key)

    def refill(self):
        if self.redis_manager.exists(self.key):
            return
        for _ in range(self.size_of_bucket):
            self.redis_manager.lpush(self.key, _)
        self.redis_manager.expire(self.key, 180)
    def size(self):
        return self.redis_manager.llen(self.key)
    
    def exists(self):
        return self.redis_manager.exists(self.key)
    

def get_token_bucket(key, sizeof_bucket):
    respons = TokenBucket(redis_manager=get_redis_manager(key).redis, key=key, size_of_bucket= sizeof_bucket)
    # respons.refill()
    return respons