from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ObjectBase(BaseModel):
    key: int
    Expires: Optional[datetime] = None


class ObjectCreate(ObjectBase):
    def to_json(self):
        return {
            "key": self.key,
        }


class Object(ObjectBase):
    id: int

    class Config:
        orm_mode = True
