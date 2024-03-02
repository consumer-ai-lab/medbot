import redis
import json

class RedisManager:
    def __init__(
            self,
            session_id:str,
            redis_url,
            redis_port,
            chats_life_time
        ):
        self.history = redis.Redis(
            host=redis_url,
            port=redis_port,
            decode_responses=True
        )
        self.user_session_id=session_id
        self.chats_life_time=chats_life_time

    @property
    def key(self):
        return "message_store:"+self.user_session_id

    def add_user_message(self,message:str):
        self.history.lpush(self.key,json.dumps(message_to_dict(message=message,type='human')))
        if self.chats_life_time:
            self.history.expire(self.key,self.chats_life_time)
    
    def add_ai_message(self,message:str):
        self.history.lpush(self.key,json.dumps(message_to_dict(message=message,type='ai')))
        if self.chats_life_time:
            self.history.expire(self.key,self.chats_life_time)

    def delete_chats(self):
        self.history.delete(self.key)

    def get_messages(self):
        messages = self.history.lrange(self.key,0,-1)
        return [] if messages is None else list(map(json.loads, messages))[::-1]
    
        
def message_to_dict(message,type):
    return {"type":type,"content":message}

def get_redis_manager(session_id: str, redis_url: str = None, redis_port: int = None, chats_life_time: int = None) -> RedisManager:
    _redis_url = redis_url if redis_url is not None else 'redis-service'
    _redis_port = redis_port if redis_port is not None else 6379
    _chats_life_time = chats_life_time if chats_life_time is not None else 6000
    return RedisManager(session_id=session_id,redis_url=_redis_url,redis_port=_redis_port,chats_life_time=_chats_life_time)