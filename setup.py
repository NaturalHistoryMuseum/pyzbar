#!/usr/bin/env python
import sys

import pyzbar


SCRIPTS = ['read_zbar']

# Optional dependency
PILLOW = 'Pillow>=3.2.0'

URL = 'https://github.com/NaturalHistoryMuseum/pyzbar/'


def readme():
    try:
        # README.rst is generated from README.md (see DEVELOPING.md)
        with open('README.rst') as f:
            return f.read()
    except:
        return 'Visit {0} for more details.'.format(URL)


setup_data = {
    'name': 'pyzbar',
    'version': pyzbar.__version__,
    'author': 'Lawrence Hudson',
    'author_email': 'l.hudson@nhm.ac.uk',
    'url': URL,
    'license': 'MIT',
    'description': pyzbar.__doc__,
    'long_description': readme(),
    'packages': ['pyzbar', 'pyzbar.scripts', 'pyzbar.tests'],
    'test_suite': 'pyzbar.tests',
    'scripts': ['pyzbar/scripts/{0}.py'.format(script) for script in SCRIPTS],
    'entry_points': {
        'console_scripts':
            ['{0}=pyzbar.scripts.{0}:main'.format(script) for script in SCRIPTS],
    },
    'extras_require': {
        ':python_version=="2.7"': ['enum34>=1.1.6', 'pathlib>=1.0.1'],
        'scripts': [
            PILLOW,
        ],
    },
    'tests_require': [
        # TODO How to specify OpenCV? 'cv2>=2.4.8,<3',
        'nose>=1.3.4',
        PILLOW
    ],
    'include_package_data': True,
    'package_data': {'pyzbar': ['pyzbar/tests/*.png']},
    'classifiers': [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
}


if 'bdist_wheel' in sys.argv and ('--plat-name=win32' in sys.argv or '--plat-name=win_amd64' in sys.argv):
    # Include the pyzbar runtime DLL, its dependencies and its license in
    # 'data_files'
    from pathlib import Path
    dir = Path(
        'dlls-{0}'.format('32' if '--plat-name=win32' in sys.argv else '64')
    )
    data_files = setup_data.get('data_files', [])
    data_files.append(
        ('', ['zbar-LICENSE.txt'] + [str(p) for p in dir.glob('*dll')])
    )
    setup_data['data_files'] = data_files


def setuptools_setup():
    from setuptools import setup
    setup(**setup_data)


if (2, 7) == sys.version_info[:2] or (3, 4) <= sys.version_info:
    setuptools_setup()
else:
    sys.exit('Python versions 2.7 and >= 3.4 are supported')
