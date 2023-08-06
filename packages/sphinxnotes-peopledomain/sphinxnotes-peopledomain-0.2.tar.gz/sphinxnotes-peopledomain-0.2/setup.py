# -*- coding: utf-8 -*-
from __future__ import with_statement

from setuptools import setup, find_packages

requires = [
    'Sphinx >= 1.5',
]


def readme():
    try:
        with open('README.rst') as f:
            return f.read()
    except IOError:
        pass


setup(
    name='sphinxnotes-peopledomain',
    version='0.2',
    url='https://github.com/sphinx-notes/peopledomain',
    download_url='https://pypi.org/project/sphinxnotes-peopledomain/',
    license='BSD',
    author='Shengyu Zhang',
    # author_email='', # I dont want write it here
    description='Sphinx domain for describing people',
    long_description=readme(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxnotes'],
)
