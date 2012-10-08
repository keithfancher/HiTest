#!/usr/bin/env python


import unittest
import hitest as h


class TestToCamelCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_normal_function(self):
        func_name = "some_normal_function"
        camelized = "SomeNormalFunction"
        self.assertEqual(h.to_camel_case(func_name), camelized)


if __name__ == '__main__':
    unittest.main()
