#!/usr/bin/python3
"This is the base model"
import uuid
from datetime import datetime
from . import storage


class BaseModel:
    "BaseModel that defines all common attributes/methods for other classes"

    def __init__(self, *args, **kwargs):
        "Initializes an instance of BaseModel"
        if kwargs:
            for k, v in kwargs.items():
                if k in ['created_at', 'updated_at']:
                    fmt = '%Y-%m-%dT%H:%M:%S.%f'
                    setattr(self, k, datetime.strptime(v, fmt))
                elif k != '__class__':
                    setattr(self, k, v)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            storage.new(self)

    def __str__(self):
        "Returns the string representation of an instance"
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        "Updates the public instance attribute updated_at, and saves it"
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        "Returns the dictionary representation of the instance"
        res = dict(self.__dict__)
        res["__class__"] = self.__class__.__name__
        res["created_at"] = self.created_at.isoformat()
        res["updated_at"] = self.updated_at.isoformat()
        return res
