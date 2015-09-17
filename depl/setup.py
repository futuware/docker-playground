# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='depl',
    version='0.1',
    description='Futurico deployment util',
    packages=['depl'],
    install_requires=[
        'plumbum==1.5.0',
    ],
    entry_points={
        'console_scripts': ['depl = depl:main'],
    },
)
