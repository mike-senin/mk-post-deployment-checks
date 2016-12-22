# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='salt-mk-verificator',
    version='0.0.1',
    description='set of tools for MK deployments verification',
    long_description=readme,
    author='Michael Senin',
    author_email='msenin94@gmail.com',
    url='https://github.com/msenin94/salt-mk-verificator',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

