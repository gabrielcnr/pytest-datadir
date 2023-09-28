import io

from setuptools import find_packages
from setuptools import setup

with io.open("README.md", encoding="UTF-8") as fp:
    long_description = fp.read()


setup(
    name="pytest-datadir",
    use_scm_version={"write_to": "src/pytest_datadir/_version.py"},
    packages=find_packages(where="src"),
    entry_points={
        "pytest11": ["pytest-datadir = pytest_datadir.plugin"],
    },
    package_dir={"": "src"},
    setup_requires=["setuptools_scm"],
    install_requires=["pytest>=5.0"],
    author="Gabriel Reis",
    author_email="gabrielcnr@gmail.com",
    description="pytest plugin for test data directories and files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="pytest test unittest directory file",
    url="http://github.com/gabrielcnr/pytest-datadir",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
)
