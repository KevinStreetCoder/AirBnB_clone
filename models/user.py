#!/usr/bin/python3
"User module"
from .base_model import BaseModel


class User(BaseModel):
    "User class"

    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *args, **kwargs):
        super().__init__(self, **kwargs)
