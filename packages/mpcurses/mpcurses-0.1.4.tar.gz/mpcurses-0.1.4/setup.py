#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'mpcurses',
        version = '0.1.4',
        description = 'A framework that exposes a simple set of APIs enabling multi-process integration with the curses screen painting library',
        long_description = '\nMpcurses is an abstraction of the Python curses and multiprocessing libraries providing function execution and runtime visualization capabilities at scale. It contains a simple API to enable any Python function to be executed across one or more background processes and includes built-in directives to visualize the functions execution on a terminal screen. \nThe mpcurses API allows for seamless integration since it does not require the target function to include additional context about curses or multiprocessing. The target function does need to implement logging since log messages are the primary means of inter-process communication between the background processes executing the function and the main process updating the curses screen on the terminal.\nFor examples checkout our home page: https://github.com/soda480/mpcurses\n',
        author = 'Emilio Reyes',
        author_email = 'emilio.reyes@intel.com',
        license = 'Apache License, Version 2.0',
        url = 'https://github.com/soda480/mpcurses',
        scripts = [],
        packages = ['mpcurses'],
        namespace_packages = [],
        py_modules = [],
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Environment :: Console :: Curses',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: System :: Networking',
            'Topic :: System :: Systems Administration'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        keywords = '',
        python_requires = '',
        obsoletes = [],
    )
