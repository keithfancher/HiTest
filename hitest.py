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
import imp
import inspect
import os
import sys


def fix_module_name(module_name):
    """Strip path and extension from a module's filename to make it
    importable."""
    base_name = os.path.basename(module_name)
    if base_name.endswith('.py'):
        return base_name[:-3]
    else:
        return base_name


def get_member_names(obj, member_type_predicate):
    """Get a list of member names of the specified type from the given object.
    member_type_predicate is one of the inspect module's is* methods."""
    names = []
    members = inspect.getmembers(obj, member_type_predicate)
    for name, dummy in members:
        names.append(name)
    return names


def get_function_names(module, include_main=False):
    """Return a list of functions in the given module. By default does not
    include main, 'cause who wants to test that?"""
    function_names = get_member_names(module, inspect.isfunction)
    if not include_main:
        try:
            function_names.remove('main')
        except ValueError:
            pass # if main's not in there we're good to go!
    return function_names


def get_class_names(module):
    """Returns a list of class names that live in the given module."""
    return get_member_names(module, inspect.isclass)


def get_methods_from_class(class_object):
    """Returns a list of methods that live in a given class."""
    return get_member_names(class_object, inspect.ismethod)


def get_classes_and_methods(module):
    """Returns a dictionary with each key a class defined in the passed module.
    The value of each key is a list of method names in that particular
    class."""
    class_names = get_class_names(module)
    methods = {}
    for class_name in class_names:
        class_object = getattr(module, class_name)
        class_methods = get_methods_from_class(class_object)
        methods[class_name] = class_methods
    return methods


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


def function_boilerplate(name):
    """Returns test boilerplate for a single function."""
    classy_name = to_class_case(name)
    test = "\nclass Test" + classy_name + "(unittest.TestCase):\n\n"
    test += "    def setUp(self):\n        pass\n\n"
    test += "    def test_something(self):\n        pass\n\n"
    return test


def class_boilerplate(module_name, class_name, method_list):
    """Returns test boilerplate for a single class."""
    test = "\nclass Test" + class_name + "(unittest.TestCase):\n\n"
    test += "    def setUp(self):\n"
    test += "        self.test_instance = " + module_name + "." + class_name
    test += "()\n\n"

    for method_name in method_list:
        test += "    def test_" + method_name + "(self):\n"
        test += "        pass\n\n"
    return test


def gen_test_boilerplate(module, include_main=False):
    """Given a module, returns a string of the test boilerplate for that
    module."""
    module_name = module.__name__
    header = "#!/usr/bin/env python\n\n\n"
    header += "import unittest\n"
    header += "import " + module_name + "\n\n"

    footer = "\nif __name__ == '__main__':\n"
    footer += "    unittest.main()\n"

    function_tests = ""
    function_names = get_function_names(module, include_main)
    for name in function_names:
        function_tests += function_boilerplate(name)

    class_tests = ""
    classes_and_methods = get_classes_and_methods(module)
    for class_name, method_list in classes_and_methods.items():
        class_tests += class_boilerplate(module_name, class_name, method_list)

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
    module_name = fix_module_name(args.target_module)

    try:
        imported = imp.load_source(module_name, args.target_module)
    except IOError:
        print "Sorry, that module doesn't seem to exist."
        sys.exit(1)
    except SyntaxError:
        print "That doesn't seem to be a valid Python module!"
        sys.exit(1)

    print gen_test_boilerplate(imported, args.test_main),


if __name__ == '__main__':
    main()
