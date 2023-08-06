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
        version = '0.1.3',
        description = 'A framework that exposes a simple set of APIs enabling multi-process integration with the curses screen painting library',
        long_description = '\nThe mpcurses provides a framework that enables a function to be executed at scale and its execution to be visualized on screen at runtime. It consists of a simple set of APIs that provide an abstraction for multiprocessing and the curses screen painting library. The main features:\n\n* Execute a function across one or more concurrent processes\n* Queue execution to ensure a predefined number of processes are running\n* Visualize function execution using curses screen\n* Define a screen layout using a Python dict\n* Leverage built-in directives for dynamically updating the screen\n  * Keep numeric counts\n  * Update text values\n  * Update text colors\n  * Maintain visual indicators\n  * Update progress bars\n  * Display tables\n\nThe framework can be used on any ordinary Python function. The only requirement for enabling function scale and execution visualization is to ensure the function implements logging and a to provide a screen layout definition. The framework takes care of setting up the multiprocessing, configuring the curses screen and the maintaining the thread-safe queues required for communication.\n\n\nRefer to [How It Works](https://github.com/soda480/mpcurses/wiki/How-It-Works) for additional detail.\n\n\nRefer to [API Reference](https://github.com/soda480/mpcurses/wiki/API-Reference) for description of the API methods and the screen layout directives.\n\n\nFor samples checkout our home page: https://github.com/soda480/mpcurses\n',
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
