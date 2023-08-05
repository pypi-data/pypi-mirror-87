# -*- coding: utf8 -*-

"""
A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
# rm dist/* && python3 setup.py sdist bdist_wheel && twine upload dist/*

from setuptools import setup, find_packages


setup(
    name='sisaptoolsDev',
    version='0.0.16',
    description='Eines per debugejar sisaptools (random-Stubs)',
    long_description="Database is faked returning random values with some logic. \
                        Mail and SSH prints the output. \
                        Redis works normal (for now)",
    url='',
    author='SIDIAP',
    author_email='',
    license='MIT',
    install_requires=[
        'python-dateutil'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Debuggers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='database development debugin Stubs',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    package_data={'': ['*.json']}
)
