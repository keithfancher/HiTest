#!/usr/bin/env python


import unittest
import hitest as h


class TestGetFunctionNames(unittest.TestCase):

    def test_with_main(self):
        """Should return all the functions, including main."""
        module = 'example_module'
        should_return = ['some_function', 'another_function',
                         'one_more_function', 'main']
        names = h.get_function_names(module, True)
        self.assertEqual(sorted(names), sorted(should_return))

    def test_ignore_main(self):
        """Should return all functions *except* for main."""
        module = 'example_module'
        should_return = ['some_function', 'another_function',
                         'one_more_function']
        names = h.get_function_names(module)
        self.assertEqual(sorted(names), sorted(should_return))

    def test_with_classes(self):
        """Should also include class methods."""
        # TODO
        pass


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


if __name__ == '__main__':
    unittest.main()
