#!/usr/bin/env python3
# -- coding: utf-8 --
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pymathtest',
    version='0.1.1.dev4',
    description='A tool that can randomly generates simple add and subtract questions.',
    long_description=long_description,
    url='https://github.com/whattobuild/pymathtest',
    author='Telon Chyi',
    author_email='laoqizhuzhanghaoyong02@outlook.com',
    packages=setuptools.find_packages(),
    classifiers=[
        "Operating System :: OS Independent",
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.4',
    keywords='maths question python',
)
