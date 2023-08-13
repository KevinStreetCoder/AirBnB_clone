#!/usr/bin/python3
"City module"
from .base_model import BaseModel


class City(BaseModel):
    "City class"
    state_id = ""
    name = ""

    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
