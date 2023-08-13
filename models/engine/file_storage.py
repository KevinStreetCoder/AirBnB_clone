#!/usr/bin/python3
"File Storage engine"
import json


class FileStorage:
    """serializes instances to a JSON file and deserializes JSON
    file to instances.

    Attributes:
        __file_path (str): Path to the JSON file.
        __objects (dict): Stores all objects.
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        "Returns the dictionary '__objects'"
        return FileStorage.__objects

    def new(self, obj):
        "Adds 'obj' to the dictionary '__objects'"
        key = obj.__class__.__name__ + '.' + obj.id
        FileStorage.__objects[key] = obj

    def save(self):
        "Serializes '__objects' to the JSON file"
        with open(FileStorage.__file_path, 'w') as file:
            new_dict = dict(FileStorage.__objects)
            for k, v in FileStorage.__objects.items():
                new_dict[k] = v.to_dict()
            json.dump(new_dict, file)

    def reload(self):
        "Deserializes the JSON file to __objects"
        from ..base_model import BaseModel
        from ..user import User
        from ..place import Place
        from ..state import State
        from ..city import City
        from ..amenity import Amenity
        from ..review import Review

        classes = {'BaseModel': BaseModel,
                   'User': User,
                   'Place': Place,
                   'State': State,
                   'City': City,
                   'Amenity': Amenity,
                   'Review': Review}
        try:
            with open(FileStorage.__file_path, 'r') as file:
                new_dict = json.load(file)
                for k, v in new_dict.items():
                    obj = classes[v['__class__']](**v)
                    FileStorage.__objects[k] = obj
        except FileNotFoundError:
            pass
