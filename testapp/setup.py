# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="testapp",
    version="0.1",
    description="Example application to play around with docker",
    packages=['testapp'],
    install_requires=[
        "pyramid==1.5.7",
    ],
    entry_points={
        'console_scripts': [
            'run-the-app = testapp.server:main'
        ]
    },
)
