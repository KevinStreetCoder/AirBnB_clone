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


class HBNHCommand(cmd.Cmd):
    """Command interpreter implementarion

    Attributs:
        prompt (str): The prompt issued to solicit input.
        classnames (list): List containing class names.
    """
    prompt = '(hbnh) '

    classnames = ['BaseModel', 'User', 'Place', 'State',
                  'City', 'Amenity', 'Review']

    def do_quit(self, line):
        "Quit command to exit the program"
        return True

    def do_EOF(self, line):
        "EOF (Ctrl + D) command to exit the program"
        return True

    def emptyline(self):
        "emptyline command to ignore 'ENTER' key"
        pass

    def valid_input(self, line, has_id=False, has_attr=False):
        """Validates the input given by the user

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
        elif args[0] not in HBNHCommand.classnames:
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
        "Creates a new instance of the given class"
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
        "Prints info of an instance based on the class name and id"
        if self.valid_input(line, True):
            key = line.split()[0] + '.' + line.split()[1]
            print(storage.all()[key])

    def do_destroy(self, line):
        "Deletes an instance based on the class name and id"
        if self.valid_input(line, True):
            key = line.split()[0] + '.' + line.split()[1]
            del storage.all()[key]
            storage.save()

    def do_all(self, line):
        "Prints all infos of all instances based or not on the class name"
        if len(line.split()) == 1 and line not in HBNHCommand.classnames:
            print("** class doesn't exist **")
            return
        objects = storage.all()
        list_objs = []
        for k, v in objects.items():
            if k.startswith(line):
                list_objs.append(str(v))
        if list_objs:
            print(list_objs)

    def do_update(self, line):
        "Updates an instance based on the class name and id"
        args = line.split()
        if self.valid_input(line, True, True):
            key = args[0] + '.' + args[1]
            obj = storage.all()[key]
            if args[3][0] in "\"'" and args[3][-1] in "\"'":
                setattr(obj, args[2], args[3][1:-1])
            elif bool(re.search(r"[0-9]+\.[0-9]", args[3])):
                setattr(obj, args[2], float(args[3]))
            else:
                setattr(obj, args[2], int(args[3]))
            storage.save()

    def default(self, line):
        "Handels the special commands"
        cmds = {'all': self.do_all,
                'count': self.count,
                'show': self.do_show,
                'destroy': self.do_destroy,
                'update': self.do_update}
        try:
            match = re.findall(r'(\w+)\.(\w+)\((.*)\)', line)[0]
        except IndexError:
            print("*** Unknown syntax: ", line)
            return
        class_name = match[0]
        cmd_name = match[1]
        _id = match[2]
        print(f"class: {class_name}\ncmd: {cmd_name}\nid: {_id}")
        args = class_name
        if _id:
            args += ' ' + _id.replace(',', '')
        cmds[cmd_name](args)

    def count(self, line):
        "Retrieve the number of instances of a class"
        count = 0
        for k in storage.all():
            if line.split()[0] in k:
                count += 1
        print(count)


if __name__ == '__main__':
    HBNHCommand().cmdloop()
