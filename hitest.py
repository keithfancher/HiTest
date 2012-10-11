#!/usr/bin/env python


# Copyright 2012 Keith Fancher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import argparse
import inspect
import sys


def fix_module_name(module):
    """Strip .py from a module name, if it exists."""
    if module.endswith('.py'):
        return module[:-3]
    else:
        return module


def get_function_names(module, include_main=False):
    """Return a list of functions in the given module. By default does not
    include main, 'cause who wants to test that?"""
    function_names = []
    imported = None
    try:
        exec('import ' + module + ' as imported') # crazy!
    except ImportError:
        print "Sorry, can't find a module called " + module
        sys.exit(1)
    funcs = inspect.getmembers(imported, inspect.isfunction)
    for name, dummy in funcs:
        if include_main or name != 'main':
            function_names.append(name)
    return function_names


def get_classes_and_methods(module):
    """Returns a dictionary with each key a class defined in the passed module.
    The value of each key is a list of method names in that particular
    class."""
    class_names = get_class_names(module)
    methods = {}
    imported = None
    try:
        exec('import ' + module + ' as imported') # crazy!
    except ImportError:
        print "Sorry, can't find a module called " + module
        sys.exit(1)
    for class_name in class_names:
        class_object = getattr(imported, class_name)
        class_methods = get_methods_from_class(class_object)
        methods[class_name] = class_methods
    return methods


def get_class_names(module):
    """Returns a list of class names that live in the given module."""
    class_names = []
    imported = None
    try:
        exec('import ' + module + ' as imported') # crazy!
    except ImportError:
        print "Sorry, can't find a module called " + module
        sys.exit(1)
    classes = inspect.getmembers(imported, inspect.isclass)
    for name, dummy in classes:
        class_names.append(name)
    return class_names


def get_methods_from_class(class_name):
    """Returns a list of methods that live in a given class."""
    method_names = []
    methods = inspect.getmembers(class_name, inspect.ismethod)
    for name, dummy in methods:
        method_names.append(name)
    return method_names


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


def gen_test_boilerplate(module_name, include_main=False):
    """This does most of the work. Given a module name, returns a string of the
    test boilerplate for that module."""
    module_name = fix_module_name(module_name) # strip .py
    header = "#!/usr/bin/env python\n\n\n"
    header += "import unittest\n"
    header += "import " + module_name + "\n\n"

    footer = "\nif __name__ == '__main__':\n"
    footer += "    unittest.main()\n"
    function_tests = ""

    function_names = get_function_names(module_name, include_main)

    for name in function_names:
        classy_name = to_class_case(name)
        function_tests += "\nclass Test" + classy_name + "(unittest.TestCase):\n\n"
        function_tests += "    def setUp(self):\n        pass\n\n"
        function_tests += "    def test_something(self):\n        pass\n\n"

    class_tests = ""
    classes_and_methods = get_classes_and_methods(module_name)
    for class_name, method_list in classes_and_methods.items():
        class_tests += "\nclass Test" + class_name + "(unittest.TestCase):\n\n"
        class_tests += "    def setUp(self):\n"
        class_tests += "        self.test_instance = " + module_name + "." + class_name + "()\n\n"

        for method_name in method_list:
            class_tests += "    def test_" + method_name + "(self):\n"
            class_tests += "        pass\n\n"

    return header + function_tests + class_tests + footer


def get_args():
    """Gets and parses command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--test-main', action='store_true',
                        default=False, help='include main function in tests')
    parser.add_argument('target_module', action='store',
                        help='the module you\'d like to generate tests for')
    return parser.parse_args()


def main():
    """My main() man."""
    args = get_args()
    print gen_test_boilerplate(args.target_module, args.test_main),


if __name__ == '__main__':
    main()
