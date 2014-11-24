import codecs
import os
import sys
import re

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

long_description = read('README.rst')

setup(
    name = "orgnote",
    version = find_version("orgnote", "__init__.py"),
    keywords = ('org-mode', 'emacs','orgnote','blog'),
    description = ' A simple blog based on org-mode',
    long_description=long_description,
    license = 'GPL',


    author = 'Leslie Zhu',
    author_email = 'czhu@kdsglobal.com',
    url = 'https://github.com/LeslieZhu/OrgNote',

    packages = find_packages(),
    package_dir = {'orgnote':'orgnote',
               },
                   
    package_data = {'': ['*.*']},


    include_package_data = True,
    platforms = 'linux',
    zip_safe=False,

    tests_require=['pytest'],
    #install_requires = ['PyYAML'],

    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 3 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GPL",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    
    entry_points={
        "console_scripts": [
            "orgnote=orgnote:main",
            "orgnote%s=orgnote:main" % sys.version[:1],
            "orgnote%s=orgnote:main" % sys.version[:3],
        ],
    },

    extras_require={
        'testing': ['pytest'],
    }
    
)