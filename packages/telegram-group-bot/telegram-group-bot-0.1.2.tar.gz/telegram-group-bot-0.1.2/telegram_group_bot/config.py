from __future__ import annotations

import toml
from pydantic import BaseModel


class Config(BaseModel):
    token: str
    welcome_message: str

    @classmethod
    def from_toml_file(cls, path: str) -> Config:
        with open(path) as f:
            return Config(**toml.load(f))
