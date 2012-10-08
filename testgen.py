#!/usr/bin/env python


import inspect


TEST_MODULE = 'example_module'


def get_function_names(module):
    """Return a list of functions in the given module."""
    function_names = []
    exec('import ' + TEST_MODULE + ' as imported') # crazy!
    funcs = inspect.getmembers(imported, inspect.isfunction)
    for key, val in funcs:
        function_names.append(key)
    return function_names


def main():
    """My main() man."""
    names = get_function_names(TEST_MODULE)
    for name in names:
        print name


if __name__ == '__main__':
    main()
