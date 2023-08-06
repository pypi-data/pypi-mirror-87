# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

NAME = 'librefi'
DESCRIPTION = 'LibreFi logs into public Wi-Fis without user interaction. Just access the network!'
URL = 'https://git.sakamoto.pl/laudom/librefi'
EMAIL = 'librefi@selfisekai.rocks'
AUTHOR = 'Lauren Liberda'
REQUIRES_PYTHON = '~=2.7, >=3.5'

REQUIRED = [
    'requests',
]

EXTRAS = {
    # 'traffic debugging': ['mitmproxy'],
}

# Get the version without importing the package (copied from youtube-dl)
exec(compile(open('librefi/version.py').read(),
             'librefi/version.py', 'exec'))

VERSION = __version__

try:
    with io.open('README.md', encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m%s\033[0m' % (s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree('dist')
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('%s setup.py sdist bdist_wheel --universal' % (sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v%s' % (VERSION))
        os.system('git push v%s' % (VERSION))

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    py_modules=['librefi'],
    entry_points={
        'console_scripts': ['librefi=librefi:main'],
    },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='GPL-3.0-or-later',
    classifiers=[
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: Jython',
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
