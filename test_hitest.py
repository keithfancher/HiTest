#!/usr/bin/env python


import unittest
import hitest as h
import test_data.example_module as test_module


class TestFixModuleName(unittest.TestCase):

    def test_with_py(self):
        """Module with .py at the end should lose the .py!"""
        module = 'some_module.py'
        output = 'some_module'
        self.assertEqual(h.fix_module_name(module), output)

    def test_with_no_py(self):
        """Module with no .py at the end should be left alone."""
        module = 'some_module'
        self.assertEqual(h.fix_module_name(module), module)


class TestGetFunctionNames(unittest.TestCase):

    def test_with_main(self):
        """Should return all the functions, including main."""
        should_return = ['some_function', 'another_function',
                         'one_more_function', 'main']
        names = h.get_function_names(test_module, True)
        self.assertEqual(sorted(names), sorted(should_return))

    def test_ignore_main(self):
        """Should return all functions *except* for main."""
        should_return = ['some_function', 'another_function',
                         'one_more_function']
        names = h.get_function_names(test_module)
        self.assertEqual(sorted(names), sorted(should_return))


class TestGetClassNames(unittest.TestCase):

    def test_blah_blah_blah(self):
        """All classes should be returned, etc. etc."""
        should_return = ['SomeClass', 'MoreDifferentClass']
        classes = h.get_class_names(test_module)
        self.assertEqual(sorted(classes), sorted(should_return))


class TestGetMethodsFromClass(unittest.TestCase):

    def test_one_method(self):
        """A class with one method should return the proper list."""
        should_return = ['some_method']
        methods = h.get_methods_from_class(test_module.SomeClass)
        self.assertEqual(sorted(methods), sorted(should_return))

    def test_more_methods(self):
        """A class with a couple of methods should return the proper list."""
        should_return = ['method_one', 'method_two']
        methods = h.get_methods_from_class(test_module.MoreDifferentClass)
        self.assertEqual(sorted(methods), sorted(should_return))


class TestGetClassesAndMethods(unittest.TestCase):

    def test_em_okay_jeez_guys(self):
        """A module with a couple of classes/methods should return the proper
        dictionary, duh."""
        should_return = { 'MoreDifferentClass': ['method_one', 'method_two'],
                          'SomeClass': ['some_method'] }
        classes_and_methods = h.get_classes_and_methods(test_module)
        self.assertEqual(classes_and_methods, should_return)


class TestToClassCase(unittest.TestCase):

    def test_normal_name(self):
        """A regular Pythonic function name should be converted."""
        func_name = "some_normal_function"
        classy = "SomeNormalFunction"
        self.assertEqual(h.to_class_case(func_name), classy)

    def test_classy_name(self):
        """An-already classy name should be left alone."""
        classy = "SomeNormalFunction"
        self.assertEqual(h.to_class_case(classy), classy)

    def test_camel_case(self):
        """A camel case name should be classified properly."""
        camel = "someFunctionName"
        classy = "SomeFunctionName"
        self.assertEqual(h.to_class_case(camel), classy)


class TestGenTestBoilerplate(unittest.TestCase):

    def test_example_module(self):
        good_boilerplate = ''
        with open('test_data/test_example_module.py') as f:
            good_boilerplate = f.read()
        self.assertEqual(h.gen_test_boilerplate(test_module), good_boilerplate)


if __name__ == '__main__':
    unittest.main()
