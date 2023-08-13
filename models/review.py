#!/usr/bin/python3
"Review module"
from .base_model import BaseModel


class Review(BaseModel):
    "Review class"

    place_id = ""
    user_id = ""
    text = ""

    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
