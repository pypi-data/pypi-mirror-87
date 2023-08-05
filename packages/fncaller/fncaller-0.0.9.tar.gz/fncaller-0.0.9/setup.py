# coding=utf-8

from distutils.core import setup
import fncaller

setup(
    name="fncaller",
    version=fncaller.version,
    python_requires='>=3.6',
    description='Python Rpc Caller For Function Server',
    author='xingyue',
    author_email='qixingyue@126.com',
    packages=[
        "fncaller"
    ],
    install_requires=[
        "requests", "dnspython"
    ]
)
