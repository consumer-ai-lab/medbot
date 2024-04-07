import redis
import json
import enum
import pydantic
from typing import List


class MessageRole(str, enum.Enum):
    user = "user"
    assistant = "assistant"

class Message(pydantic.BaseModel):
    role: MessageRole
    content: str


class RedisManager:
    def __init__(self, session_id: str, redis_url, redis_port, chats_life_time):
        self.history = redis.Redis(
            host=redis_url, port=redis_port, decode_responses=True
        )
        self.user_session_id = session_id
        self.chats_life_time = chats_life_time

    @property
    def key(self):
        return "message_store:" + self.user_session_id

    def add_message(self, message: Message):
        self.history.lpush(self.key, message.json())
        if self.chats_life_time:
            self.history.expire(self.key, self.chats_life_time)

    def delete_chats(self):
        self.history.delete(self.key)

    def get_messages(self) -> List[Message]:
        messages = self.history.lrange(self.key, 0, -1)
        return [] if messages is None else list(map(Message.model_validate_json, messages))[::-1]

def get_redis_manager(
    session_id: str,
    redis_url: str = "redis-service",
    redis_port: int = 6379,
    chats_life_time: int = 300,
) -> RedisManager:
    return RedisManager(
        session_id,
        redis_url,
        redis_port,
        chats_life_time,
    )
