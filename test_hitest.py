#!/usr/bin/env python


import unittest
import hitest as h


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
        module = 'test_data.example_module'
        should_return = ['some_function', 'another_function',
                         'one_more_function', 'main']
        names = h.get_function_names(module, True)
        self.assertEqual(sorted(names), sorted(should_return))

    def test_ignore_main(self):
        """Should return all functions *except* for main."""
        module = 'test_data.example_module'
        should_return = ['some_function', 'another_function',
                         'one_more_function']
        names = h.get_function_names(module)
        self.assertEqual(sorted(names), sorted(should_return))


class TestGetMethodNames(unittest.TestCase):

    def test_one_method(self):
        """A class with one method should return the proper dictionary, duh."""
        module = 'test_data.example_module'
        should_return = { 'SomeClass': ['some_method'] }
        methods = h.get_method_names(module)
        self.assertEqual(sorted(methods), sorted(should_return))


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
        module = 'test_data.example_module'
        good_boilerplate = ''
        with open('test_data/test_example_module.py') as f:
            good_boilerplate = f.read()
        self.assertEqual(h.gen_test_boilerplate(module), good_boilerplate)


if __name__ == '__main__':
    unittest.main()
