import io
import re

from setuptools import setup


with io.open('README.md', encoding='UTF-8') as fp:
    long_description = fp.read()


setup(
    name="pytest-datadir",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=['pytest_datadir'],
    entry_points={
        'pytest11': ['pytest-datadir = pytest_datadir.plugin'],
    },
    install_requires=['pytest>=2.7.0'],
    data_files = [("", ["LICENSE"])],
    author='Gabriel Reis',
    author_email='gabrielcnr@gmail.com',
    description='pytest plugin for test data directories and files',
    long_description=long_description,
    long_description_content_type="text/markdown",

    license='MIT',
    keywords='pytest test unittest directory file',
    extras_require={':python_version<"3.4"': ['pathlib2']},
    url='http://github.com/gabrielcnr/pytest-datadir',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
    ],
)
