import re

from setuptools import setup


with open('pytest_datadir/__init__.py') as fp:
    m = re.search("version = '(.*)'", fp.read())
    assert m is not None
    version = m.group(1)


setup(
    name="pytest-datadir",
    version=version,
    packages=['pytest_datadir'],
    entry_points={
        'pytest11': ['pytest-datadir = pytest_datadir.plugin'],
    },
    install_requires=['pytest>=2.7.0'],

    author='Gabriel Reis',
    author_email='gabrielcnr@gmail.com',
    description='pytest plugin for test data directories and files',
    license='MIT',
    keywords='pytest test unittest directory file',
    extras_require={':python_version<"3.4"': ['pathlib']},
    url='http://github.com/gabrielcnr/pytest-datadir',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
    ],
)
