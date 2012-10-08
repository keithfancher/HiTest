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


import inspect


TEST_MODULE = 'test_data.example_module'


def get_function_names(module, include_main=False):
    """Return a list of functions in the given module. Does not include main()
    by default."""
    function_names = []
    exec('import ' + module + ' as imported') # crazy!
    funcs = inspect.getmembers(imported, inspect.isfunction)
    for key, val in funcs:
        if include_main or key != 'main':
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


def gen_test_boilerplate(module_name):
    """This does most of the work. Given a module name, returns a string of the
    test boilerplate for that module."""
    header = "#!/usr/bin/env python\n\n\n"
    header += "import unittest\n"
    header += "import " + module_name + "\n\n\n"

    footer = "if __name__ == '__main__':\n"
    footer += "    unittest.main()\n"
    classes = ""

    function_names = get_function_names(module_name)

    for name in function_names:
        classy_name = to_class_case(name)
        classes += "class Test" + classy_name + "(unittest.TestCase):\n\n"
        classes += "    def setUp(self):\n        pass\n\n"
        classes += "    def test_something(self):\n        pass\n\n\n"

    return header + classes + footer


def main():
    """My main() man."""
    pass


if __name__ == '__main__':
    main()
