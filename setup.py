import os
import shutil
import zipfile

from setuptools import setup, find_packages

from distutils.cmd import Command
try: # for pip >= 10
    from pip._internal.commands import WheelCommand
except ImportError: # for pip <= 9.0.3
    from pip.commands import WheelCommand

try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements


PACKAGE_NAME = 'connectedCars'
VERSION = '0.1'

with open("README.md", "r") as fh:
    long_description = fh.read()


reqs = parse_requirements('requirements.txt', session=False)
requirements = [str(ir.req) for ir in reqs]

test_reqs = parse_requirements('test_requirements.txt', session=False)
test_requirements = [str(ir.req) for ir in test_reqs]


setup(
    name=PACKAGE_NAME,

    version=VERSION,

    description='ConnectedCars',
    
    long_description=long_description,
    
    long_description_content_type="text/markdown",
    
    url="https://github.com/pypa/sampleproject",

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],

    author='Sumit kumar',

    author_email='sumit.kumar@td.com',

    

    packages=find_packages(include=['connectedCars', 'connectedCars.*'],
                           exclude=['*.test.*', '*.test']),

    install_requires=requirements,

    tests_require=test_requirements,

    package_data={
        PACKAGE_NAME: ['../requirements.txt', '../test_requirements.txt']
    }

  
)
