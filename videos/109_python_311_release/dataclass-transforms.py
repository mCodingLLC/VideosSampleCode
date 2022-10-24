from dataclasses import dataclass
from typing import dataclass_transform


@dataclass_transform
class BaseModel:
    ...

class User(BaseModel):
    id: int
    name: str


user = User(id=0, name="James")
