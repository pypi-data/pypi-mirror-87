# !/usr/bin/env python
__version__ = "1.3.0"

from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='api_jwt_2',
    version=__version__,
    description='Library for JWT encoding/decoding specifically adapted to use in APIs',
    long_description_content_type="text/markdown",
    long_description=readme(),
    author='Greger Wedel',
    author_email='greger@greger.io',
    license='Apache2',
    url='https://github.com/krystian-kulgawczuk-pr/api_jwt',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    py_modules=['api_jwt_2', ],
    install_requires=[
        'pyjwt>=1.6.1',
        'cryptography',
    ],
    include_package_data=True
)
