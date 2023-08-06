"""Setup script for QLog """

import os.path
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="QLog",
    version="0.1.0",
    description="Logger",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/QuantumApplications/QLog-Python",
    author="Quantum Applications",
    author_email="oberdoerfer@quantum.qa",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    packages=["QLog"],
    include_package_data=True,
    install_requires=[]
)
