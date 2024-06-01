import aioredis
import json

from typing import List, Sequence

from app.schemas import LessonOut
from app.models import Lesson


class RedisHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._redis = aioredis.from_url("redis://localhost")
        return cls._instance

    async def get(self, key: str):
        return await self._redis.get(key)

    async def set(self, key: str, value: str, ex: int = 3600):
        await self._redis.set(key, value, ex=ex)

    @staticmethod
    def serialize_schedule(schedule: Sequence[Lesson]) -> str:
        return json.dumps([lesson.dict() for lesson in schedule], default=str)

    @staticmethod
    def deserialize_schedule(serialized_schedule: str) -> List[LessonOut]:
        return [LessonOut(**json.loads(lesson)) for lesson in json.loads(serialized_schedule)]
