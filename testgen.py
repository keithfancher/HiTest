#!/usr/bin/env python


import inspect


TEST_MODULE = 'example_module'


def main():
    exec('import ' + TEST_MODULE + ' as imported') # crazy!
    funcs = inspect.getmembers(imported, inspect.isfunction)
    print funcs


if __name__ == '__main__':
    main()
