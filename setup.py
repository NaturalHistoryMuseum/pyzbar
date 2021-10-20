#!/usr/bin/env python
import sys

import pyzbar


SCRIPTS = ['read_zbar']

# Optional dependency
PILLOW = 'Pillow>=3.2.0'

URL = 'https://github.com/NaturalHistoryMuseum/pyzbar/'


def readme():
    # TODO IOError on Python 2.x. FileNotFoundError on Python 3.x.
    try:
        with open('README.rst') as f:
            return f.read()
    except:
        return 'Visit {0} for more details.'.format(URL)


setup_data = {
    'name': 'pyzbar',
    'version': pyzbar.__version__,
    'author': 'Lawrence Hudson',
    'author_email': 'quicklizard@googlemail.com',
    'url': URL,
    'license': 'MIT',
    'description': pyzbar.__doc__,
    'long_description': readme(),
    'long_description_content_type': 'text/x-rst',
    'packages': ['pyzbar', 'pyzbar.scripts', 'pyzbar.tests'],
    'test_suite': 'pyzbar.tests',
    'scripts': ['pyzbar/scripts/{0}.py'.format(script) for script in SCRIPTS],
    'entry_points': {
        'console_scripts': [
            '{0}=pyzbar.scripts.{0}:main'.format(script) for script in SCRIPTS
        ],
    },
    'extras_require': {
        ':python_version=="2.7"': ['enum34>=1.1.6', 'pathlib>=1.0.1'],
        'scripts': [
            PILLOW,
        ],
    },
    'tests_require': [
        # TODO How to specify OpenCV? 'cv2>=2.4.8',
        'mock>=2.0.0; python_version=="2.7"',
        'numpy>=1.8.2',
        PILLOW,
    ],
    'include_package_data': True,
    'classifiers': [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
}


def setuptools_setup():
    from setuptools import setup
    setup(**setup_data)


if (2, 7) == sys.version_info[:2] or (3, 5) <= sys.version_info:
    setuptools_setup()
else:
    sys.exit('Python versions 2.7 and >= 3.5 are supported')
