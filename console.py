#!/usr/bin/python3
"The entry point of the command interpreter"
import cmd
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage
import re
import json


class HBNBCommand(cmd.Cmd):
    """Command interpreter implementarion.

    Attributs:
        prompt (str): The prompt issued to solicit input.
        classnames (list): List containing class names.
    """
    prompt = '(hbnb) '

    classnames = ['BaseModel', 'User', 'Place', 'State',
                  'City', 'Amenity', 'Review']

    def do_quit(self, line):
        "Quit command to exit the program."
        return True

    def do_EOF(self, line):
        "EOF (Ctrl + D) command to exit the program."
        print()
        return True

    def emptyline(self):
        "emptyline command to ignore 'ENTER' key."
        pass

    def valid_input(self, line, has_id=False, has_attr=False):
        """Validates the input given by the user.

        Args:
            line (str): The user input.
            has_id (bool): Indicates if the 'line' contains an id or not.
            has_attr (bool): Indicates if the 'line' contains attributs or not.

        Returns:
            bool: True for valid input, False otherwise.
        """
        args = line.split()
        lenght = len(args)
        if lenght == 0:
            print("** class name missing **")
            return False
        elif args[0] not in HBNBCommand.classnames:
            print("** class doesn't exist **")
            return False
        elif has_id and lenght == 1:
            print("** instance id missing **")
            return False
        elif has_id and args[0] + '.' + args[1] not in storage.all():
            print("** no instance found **")
            return False
        elif has_attr and lenght == 2:
            print("** attribute name missing **")
            return False
        elif has_attr and lenght == 3:
            print("** value missing **")
            return False
        return True

    def do_create(self, line):
        "Creates a new instance of the given class.\n"
        classes = {'BaseModel': BaseModel,
                   'User': User,
                   'Place': Place,
                   'State': State,
                   'City': City,
                   'Amenity': Amenity,
                   'Review': Review}
        if self.valid_input(line):
            obj = classes[line]()
            storage.save()
            print(obj.id)

    def do_show(self, line):
        "Prints info of an instance based on the class name and id."
        if self.valid_input(line, True):
            key = line.split()[0] + '.' + line.split()[1]
            print(storage.all()[key])

    def do_destroy(self, line):
        "Deletes an instance based on the class name and id."
        if self.valid_input(line, True):
            key = line.split()[0] + '.' + line.split()[1]
            del storage.all()[key]
            storage.save()

    def do_all(self, line):
        "Prints all infos of all instances based or not on the class name."
        if len(line.split()) == 1 and line not in HBNBCommand.classnames:
            print("** class doesn't exist **")
            return
        objects = storage.all()
        list_objs = []
        for k, v in objects.items():
            if k.startswith(line):
                list_objs.append(str(v))
        if list_objs:
            print(list_objs)

    def do_update(self, line, type_flag=None):
        "Updates an instance based on the class name and id."
        args = line.split()
        if self.valid_input(line, True, True):
            key = args[0] + '.' + args[1]
            obj = storage.all()[key]
            setattr(obj, str(args[2]), self.type_caste(args[3],
                    type_flag)(args[3]))
            storage.save()

    def default(self, line):
        "Handels the special commands."
        cmds = {'all': self.do_all,
                'count': self.count,
                'show': self.do_show,
                'destroy': self.do_destroy,
                'update': self.do_update}
        info = dict()
        try:
            match = re.findall(r'(\w+)\.(\w+)\((.*)\)', line)[0]
            info['id'] = ' ' + re.search(r'"([^"]*)"', match[2]).group(1)
        except IndexError:
            return
        except AttributeError:
            info['id'] = ''

        info['class'] = match[0]
        info['cmd'] = match[1]

        if info['cmd'] == 'update':
            if '{' in match[2] and match[2].endswith('}'):
                attrs = line[line.index('{'):line.index('}') + 1]
                attrs = json.loads(attrs.replace("'", '"'))
                info['attrs'] = attrs
            else:
                res = match[2].split(',')
                info['attrs'] = {res[1]: res[2]}
            for k, v in info['attrs'].items():
                k = k.replace("'", "").replace('"', '')
                cmds[info['cmd']](info['class'] + info['id'] +
                                  ' ' + k + ' ' + str(v), type(v))
        else:
            cmds[info['cmd']](info['class'] + info['id'])

    def count(self, line):
        "Retrieve the number of instances of a class."
        if self.valid_input(line):
            count = 0
            for k in storage.all():
                if line.split()[0] in k:
                    count += 1
            print(count)

    def type_caste(self, value, flag):
        if flag:
            return flag
        elif value.replace('.', '', 1).isdigit():
            return float
        elif value.isdigit():
            return int
        else:
            return str


if __name__ == '__main__':
    HBNBCommand().cmdloop()
