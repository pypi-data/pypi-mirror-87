# !/usr/bin/env python
import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
with open('requirements-test.txt') as f:
    test_requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("VERSION", "r") as buf:
    version = buf.read()

setuptools.setup(
    name="cyjax-cti",
    version=version,
    license="MIT",
    description="cyjax-cti provides a Python library to use Cyjax platform API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Cyjax Ltd.",
    author_email="github@cyjax.com",
    url="https://www.cyjax.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development",
    ],
    packages=setuptools.find_packages(),
    extras_require={
        "test": test_requirements
    },
    install_requires=requirements,
)
