import redis
from typing import List
import json
from .types import Message, ChatThread


class RedisManager:
    def __init__(self, user_id: str, redis_url, redis_port, chats_life_time):
        self.redis = redis.Redis(
            host=redis_url, port=redis_port, decode_responses=True
        )
        self.user_id = user_id
        self.chats_life_time = chats_life_time

    @property
    def key(self):
        return "message_store:" + self.user_id

    def thread_key(self, thread_id: str):
        return f"{self.key}:{thread_id}"

    def add_message(self, thread_id: str, message: Message):
        key = self.thread_key(thread_id)
        self.redis.lpush(key, message.json())
        if self.chats_life_time:
            self.redis.expire(self.key, self.chats_life_time)

    def delete_chats(self):
        self.redis.delete(self.key)

    def get_chat(self, thread_id: str) -> List[Message]:
        key = self.thread_key(thread_id)
        messages = self.redis.lrange(key, 0, -1)
        return [] if messages is None else list(map(Message.model_validate_json, messages))[::-1]
    
    def delete_thread(self, thread_id: str):
        thread_key = self.thread_key(thread_id)
        self.redis.delete(thread_key)
        elements = self.redis.lrange(self.key, 0, -1)
        for element in elements:
            json_obj = json.loads(element)
            if json_obj["id"] == thread_id:
                self.redis.lrem(self.key, 0, element)
                break

    def get_threads(self) -> List[ChatThread]:
        threads = self.redis.lrange(self.key, 0, -1)
        return [] if threads is None else list(map(ChatThread.model_validate_json, threads))[::-1]
    
    def has_thread(self, thread_id: str) -> bool:
        key = self.thread_key(thread_id)
        return self.redis.exists(key)

    def add_thread(self, thread: ChatThread):
        self.redis.lpush(self.key, thread.json())

def get_redis_manager(
    user_id: str,
    redis_url: str = "redis-service",
    redis_port: int = 6379,
    chats_life_time: int = 30000,
) -> RedisManager:
    return RedisManager(
        user_id,
        redis_url,
        redis_port,
        chats_life_time,
    )
