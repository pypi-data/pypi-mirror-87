#!/bin/env python

import os
import string

from setuptools import setup, find_packages


NAME = 'DejaVu Serif'
LICENSE = 'Bitstream Vera Fonts Copyright, Arev Fonts Copyright, Public Domain'

ENTRY_POINT_NAME = NAME.lower()
IDENTIFIER = ''.join(char for char in ENTRY_POINT_NAME
                     if char in string.ascii_lowercase + string.digits)
PACKAGE_NAME = 'rinoh-typeface-{}'.format(IDENTIFIER)
PACKAGE_DIR = PACKAGE_NAME.replace('-', '_')

SETUP_PATH = os.path.dirname(os.path.abspath(__file__))


setup(
    name=PACKAGE_NAME,
    version='0.1.3',
    packages=find_packages(),
    package_data={PACKAGE_DIR: ['*.ttf', '*.txt', 'AUTHORS', 'BUGS', 'LICENSE',
                                'NEWS', 'README.md']},
    install_requires=['rinohtype'],
    entry_points={
        'rinoh.typefaces':
            ['{} = {}:typeface'.format(ENTRY_POINT_NAME, PACKAGE_DIR)]
    },

    author='Brecht Machiels',
    author_email='brecht@mos6581.org',
    description='DejaVu Serif typeface',
    long_description=open(os.path.join(SETUP_PATH, 'README.rst')).read(),
    url='https://github.com/brechtm/rinoh-typeface-dejavuserif',
    keywords='opentype font',
    license=LICENSE,
    classifiers = [
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Fonts',
    ]
)
