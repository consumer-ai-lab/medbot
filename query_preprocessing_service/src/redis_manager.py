from langchain_community.chat_message_histories import RedisChatMessageHistory

class RedisManager:
    def __init__(self,session_id:str,redis_url="redis://redis-service:6379",chats_life_time=60):
        self.history = RedisChatMessageHistory(session_id=session_id,url=redis_url,ttl=chats_life_time)

    def add_user_message(self,message:str):
        self.history.add_user_message(message=message)
    
    def add_ai_message(self,message:str):
        self.history.add_ai_message(message=message)

def get_redis_manager(session_id:str):
    return RedisManager(session_id=session_id)