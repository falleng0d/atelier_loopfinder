from __future__ import annotations

from typing import List

import yaml
from pydantic import BaseModel

class Item(BaseModel):
    Name: str
    Type: List[str]
    Recipe: List[str]


class Model(BaseModel):
    items: List[Item]

def load_data(file: str) -> Model:
    with open(file) as f:
        data = Model.parse_obj(yaml.safe_load(f))
    return data
