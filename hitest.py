#!/usr/bin/env python


import inspect


TEST_MODULE = 'example_module'


def get_function_names(module, include_main=False):
    """Return a list of functions in the given module. Does not include main()
    by default."""
    function_names = []
    exec('import ' + TEST_MODULE + ' as imported') # crazy!
    funcs = inspect.getmembers(imported, inspect.isfunction)
    for key, val in funcs:
        function_names.append(key)
    return function_names


def to_class_case(name):
    """Turns some_function into SomeFunction."""
    ret = ''
    words = name.split('_')
    if len(words) > 1:
        for word in words:
            ret += word.title()
    else:
        # can't use title here, must preserve other caps
        ret = name[0].upper() + name[1:]
    return ret


def gen_test_boilerplate(module_name, function_names):
    header = """#!/usr/bin/env python\n\n
import unittest
import """ + module_name + "\n\n"
    footer = """if __name__ == '__main__':
    unittest.main()"""
    classes = ""

    for name in function_names:
        classes += "class Test_" + name + "(unittest.TestCase):\n\n"
        classes += "    def setUp(self):\n        pass\n\n"
        classes += "    def test_something(self):\n        pass\n\n\n"

    print header
    print classes
    print footer


def main():
    """My main() man."""
    names = get_function_names(TEST_MODULE)
    gen_test_boilerplate(TEST_MODULE, names)


if __name__ == '__main__':
    main()
