#!/usr/bin/env python


from distutils.core import setup


setup(name='hitest',
      version='0.1.0',
      description='Generates unit test boilerplate for Python modules',
      author='Keith Fancher',
      author_email='keith.fancher@gmail.com',
      license='GPLv3',
      url='https://github.com/keithfancher/HiTest',
      scripts=['hitest.py'],
      install_requires=[
          'argparse'
      ]
)
