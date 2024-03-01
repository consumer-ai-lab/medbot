import redis
import json

class RedisManager:
    def __init__(
            self,
            session_id:str,
            redis_url="redis-service",
            redis_port=6379,
            chats_life_time=6000
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

def get_redis_manager(session_id:str):
    return RedisManager(session_id=session_id)