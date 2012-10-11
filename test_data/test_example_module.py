#!/usr/bin/env python


import unittest
import test_data.example_module


class TestAnotherFunction(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        pass


class TestOneMoreFunction(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        pass


class TestSomeFunction(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        pass


class TestMoreDifferentClass(unittest.TestCase):

    def setUp(self):
        self.test_instance = test_data.example_module.MoreDifferentClass()

    def test_method_one(self):
        pass

    def test_method_two(self):
        pass


class TestSomeClass(unittest.TestCase):

    def setUp(self):
        self.test_instance = test_data.example_module.SomeClass()

    def test_some_method(self):
        pass


if __name__ == '__main__':
    unittest.main()
