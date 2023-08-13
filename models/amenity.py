#!/usr/bin/python3
"Amenity module"
from .base_model import BaseModel


class Amenity(BaseModel):
    "Amenity class"

    name = ""

    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
