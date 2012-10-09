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
    header += "import " + module_name + "\n\n\n"

    footer = "if __name__ == '__main__':\n"
    footer += "    unittest.main()\n"
    classes = ""

    function_names = get_function_names(module_name, include_main)

    for name in function_names:
        classy_name = to_class_case(name)
        classes += "class Test" + classy_name + "(unittest.TestCase):\n\n"
        classes += "    def setUp(self):\n        pass\n\n"
        classes += "    def test_something(self):\n        pass\n\n\n"

    return header + classes + footer


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
