#!/usr/bin/python3
""" Module for testing FileStorage class """
import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from datetime import datetime
import json
import os

class TestFileStorage(unittest.TestCase):
    """ Test cases for FileStorage class """

    def setUp(self):
        """ Set up test environment """
        self.storage = FileStorage()

    def tearDown(self):
        """ Clean up after each test """
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_empty_initialization(self):
        """ Test if the storage dictionary is empty initially """
        self.assertEqual(len(self.storage.all()), 0)

    def test_new_method(self):
        """ Test new method of FileStorage """
        model = BaseModel()
        self.storage.new(model)
        self.assertIn(f"BaseModel.{model.id}", self.storage.all())

    def test_save_method(self):
        """ Test save method of FileStorage """
        model = BaseModel()
        self.storage.new(model)
        self.storage.save()
        with open("file.json", "r") as f:
            data = json.load(f)
            key = f"BaseModel.{model.id}"
            self.assertTrue(key in data)

    def test_reload_method(self):
        """ Test reload method of FileStorage """
        model = BaseModel()
        model.save()
        self.storage.reload()
        key = f"BaseModel.{model.id}"
        self.assertTrue(key in self.storage.all())

    def test_reload_file_not_found(self):
        """ Test reload method when file doesn't exist """
        self.storage.reload()
        self.assertEqual(len(self.storage.all()), 0)

    def test_serialization(self):
        """ Test JSON serialization of objects """
        model = BaseModel()
        model.name = "TestModel"
        model.save()
        with open("file.json", "r") as f:
            data = json.load(f)
            key = f"BaseModel.{model.id}"
            self.assertTrue(key in data)
            self.assertEqual(data[key]["name"], "TestModel")
            self.assertEqual(data[key]["__class__"], "BaseModel")

    def test_deserialization(self):
        """ Test JSON deserialization to objects """
        model = BaseModel()
        model.name = "TestModel"
        model.save()
        self.storage.reload()
        key = f"BaseModel.{model.id}"
        loaded_model = self.storage.all()[key]
        self.assertEqual(model.id, loaded_model.id)
        self.assertEqual(model.created_at, loaded_model.created_at)
        self.assertEqual(model.updated_at, loaded_model.updated_at)
        self.assertEqual(model.name, loaded_model.name)
        self.assertEqual(model.to_dict(), loaded_model.to_dict())

if __name__ == "__main__":
    unittest.main()
